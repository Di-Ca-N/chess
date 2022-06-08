from . import pieces


def move_factory(board, piece, origin, target, captured_piece=None) -> "Movement":
    """Create a Movement instance with the given information

    The type of the movement can vary according to the information provided

    Arguments:
        board (ChessGame): Current state of the game
        piece (Piece): Piece to move
        origin (tuple[int, int]): Piece original position
        target (tuple[int, int]): Target position
        captured_piece (Optional[Piece]): Captured piece (if it exists)

    Return:
        An instance of Movement (or of a Movement subclass)
    """
    validation_chain = [EmptyMovement, Castling, EnPassant, Promotion, Movement]

    for movement in validation_chain:
        if movement.pre_condition(piece, origin, target, captured_piece):
            return movement(board, piece, origin, target, captured_piece)


class Movement:
    """Abstracts the movement logic

    The movement logic is abstracted using the Command design pattern,
    allowing movements to be done and undone
    """

    def __init__(self, board, piece, origin, target, captured_piece=None):
        self.board = board
        self.piece = piece
        self.origin = origin
        self.target = target
        self.capture = captured_piece is not None
        self.captured_piece = captured_piece

        self.changes_moved_state = (
            not self.piece.has_moved if self.piece is not None else True
        )

    def do(self):
        """Apply the movement to the board"""

        self.board.move_piece(self.piece, self.origin, self.target)

    def undo(self):
        """Undo the movement, restoring the board state"""

        self.board.move_piece(self.piece, self.target, self.origin)

        if self.capture:
            self.board.place_piece(self.captured_piece, self.target)

        if self.changes_moved_state:
            self.piece.has_moved = False

    def is_valid(self):
        """Check if the movement is valid.

        The following conditions are required:
        1. The origin and destination are different
        2. Exists a trajectory between origin and destination, following the piece movement
        3. The movement is not blocked by another piece
        4. If it is a capture, must be of an enemy piece
        """
        if self.origin == self.target:
            return False

        trajectory = self.piece.trajectory(self.origin, self.target, self.capture)

        # Check if the piece can reach the target position
        if not trajectory:
            return False

        # Check if the movement is not blocked
        for position in trajectory:
            if position == self.origin or position == self.target:
                continue

            if self.board[position] is not None:
                return False

        # Check if the movement captures an enemy piece
        if self.capture and self.piece.color == self.captured_piece.color:
            return False

        return True

    @staticmethod
    def pre_condition(piece, origin, target, captured_piece):
        """Test if the given information correspond to this type of movement.

        This method is meant to be overwritten by subclasses.
        """
        return True


class EmptyMovement(Movement):
    """A Movement of an empty piece (None). It is always invalid"""

    def is_valid(self):
        return False

    @staticmethod
    def pre_condition(piece, origin, target, captured_piece):
        return piece is None


class Castling(Movement):
    def __init__(
        self,
        board,
        piece,
        king_origin,
        king_target,
        captured_piece=None,
    ):
        super().__init__(board, piece, king_origin, king_target)

        _, king_initial_col = king_origin
        king_target_row, king_target_col = king_target

        self.king = piece
        self.king_position = king_origin

        # Identifying short or long castling
        if king_target_col > king_initial_col:
            # Short castling
            rook_initial_row, rook_initial_col = king_target_row, king_target_col + 1
            rook_final_row, rook_final_col = king_target_row, king_target_col - 1
        else:
            # Long castling
            rook_initial_row, rook_initial_col = king_target_row, king_target_col - 2
            rook_final_row, rook_final_col = king_target_row, king_target_col + 1

        self.rook = board[rook_initial_row, rook_initial_col]
        self.rook_position = (rook_initial_row, rook_initial_col)
        self.final_rook_position = (rook_final_row, rook_final_col)
        self.target_king_position = king_target

        # The castling involves a movement from the rook and from the king
        self.moves = [
            Movement(board, self.king, self.king_position, self.target_king_position),
            Movement(board, self.rook, self.rook_position, self.final_rook_position),
        ]

    def do(self):
        for move in self.moves:
            move.do()

    def undo(self):
        for move in reversed(self.moves):
            move.undo()

    def is_valid(self):
        if self.king is None or self.rook is None:
            return False

        if self.king.color != self.rook.color:
            return False

        if self.king.has_moved or self.rook.has_moved:
            return False

        if self.king_position[0] != self.rook_position[0]:
            return False

        # No piece between the king and the rook
        total_start, total_end = self.king_position[1], self.rook_position[1]
        if total_start > total_end:
            total_start, total_end = total_end, total_start
        for col in range(total_start + 1, total_end):
            if self.board[self.king_position[0], col] is not None:
                return False

        # The king path is not being attacked by enemy pieces
        king_start, king_end = self.king_position[1], self.target_king_position[1]
        if king_start > king_end:
            king_start, king_end = king_end, king_start

        for col in range(king_start, king_end + 1):
            king_path_square = (self.king_position[0], col)
            if self.board.verify_check(king_path_square, self.king.color):
                return False

        return True

    @staticmethod
    def pre_condition(piece, origin, target, captured_piece) -> bool:
        king_move = isinstance(piece, pieces.King)
        move_two_squares = abs(origin[1] - target[1]) == 2
        on_the_same_row = origin[0] == target[0]
        return all([king_move, move_two_squares, on_the_same_row])


class EnPassant(Movement):
    def __init__(self, board, piece, origin, target, captured_piece=None):
        super().__init__(board, piece, origin, target, captured_piece)
        try:
            self.previous_move = self.board.history[-1]
            self.captured_piece = self.previous_move.piece
        except IndexError:
            self.previous_move = None
            self.captured_piece = None

    def do(self):
        self.board.move_piece(self.piece, self.origin, self.target)
        self.board.place_piece(None, self.previous_move.target)

    def undo(self):
        self.board.move_piece(self.piece, self.target, self.origin)
        self.board.place_piece(self.captured_piece, self.previous_move.target)

    def is_valid(self):
        if self.captured_piece is None:
            return False

        is_a_pawn_move = isinstance(self.piece, pieces.Pawn)
        captured_piece_is_a_pawn = isinstance(self.captured_piece, pieces.Pawn)
        pieces_with_opposite_colors = self.captured_piece.color != self.piece.color
        captured_pawn_moved_two_squares = (
            abs(self.previous_move.target[0] - self.previous_move.origin[0]) == 2
        )
        pieces_on_the_same_row = self.previous_move.target[0] == self.origin[0]
        pieces_will_end_on_same_col = self.target[1] == self.previous_move.origin[1]
        pieces_on_adjacent_cols = (
            abs(self.previous_move.target[1] - self.origin[1]) == 1
        )

        return all(
            [
                is_a_pawn_move,
                captured_piece_is_a_pawn,
                pieces_with_opposite_colors,
                captured_pawn_moved_two_squares,
                pieces_on_the_same_row,
                pieces_will_end_on_same_col,
                pieces_on_adjacent_cols,
            ]
        )

    @staticmethod
    def pre_condition(piece, origin, target, captured_piece):
        return (
            isinstance(piece, pieces.Pawn)
            and (abs(origin[0] - target[0]) == 1 and abs(origin[1] - target[1]) == 1)
            and captured_piece is None
        )


class Promotion(Movement):
    """Promotion of a pawn

    All instances are created with the 'promotes_to' field set to None.
    You must set this field to the type of piece that pawn should
    be promoted before calling the 'do' method.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.promotes_to = None

    def do(self):
        """Promotes the pawn"""
        super().do()
        try:
            piece = self.promotes_to(color=self.piece.color, has_moved=True)
            self.board.place_piece(piece, self.target)
        except TypeError:
            raise ValueError(
                "The field 'promotes_to' must be set before calling the method 'do()'"
            )

    @staticmethod
    def pre_condition(piece, origin, target, captured_piece):
        is_pawn = isinstance(piece, pieces.Pawn)
        last_row = 0 if piece.color == pieces.Color.WHITE else 7
        going_to_last_row = target[0] == last_row

        return is_pawn and going_to_last_row
