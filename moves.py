import pieces


def process_move(board, piece, from_position, to_position, captured_piece=None):
    if (isinstance(piece, pieces.King) and abs(from_position[1] - to_position[1]) == 2):
        return Castling(board, from_position, to_position)
    if (isinstance(piece, pieces.Pawn) and (
            abs(from_position[0] - to_position[0]) == 1 and
            abs(from_position[1] - to_position[1]) == 1
        ) and captured_piece is None):
        return EnPassant(board, piece, from_position, to_position)
    return Movement(board, piece, from_position, to_position, captured_piece)


class Movement:
    def __init__(self, board, piece, from_position, to_position, captured_piece=None):
        self.board = board
        self.piece = piece
        self.from_position = from_position
        self.to_position = to_position
        self.capture = captured_piece is not None
        self.captured_piece = captured_piece
        self.changes_moved_state = not self.piece.has_moved

    def do(self):
        self.board.do_move(
            self.piece,
            self.from_position,
            self.to_position
        )

    def undo(self):
        self.board.do_move(
            self.piece,
            self.to_position,
            self.from_position
        )

        if self.capture:
            self.board[self.to_position[0]][self.to_position[1]] = self.captured_piece
        if self.changes_moved_state:
            self.piece.has_moved = False

    def is_valid(self):
        if self.capture:
            return self.piece.can_capture(self.captured_piece, self.from_position, self.to_position)

        if self.piece is None:
            return False

        movement_not_blocked = True
        exists_trajectory = True

        trajectory = self.piece.trajectory(self.from_position, self.to_position)

        if not trajectory:
            exists_trajectory = False

        for intermediate_row, intermediate_col in trajectory:
            intermediary_square = self.board[intermediate_row][intermediate_col]

            piece_exists = intermediary_square is not None
            is_initial_position = (intermediate_row, intermediate_col) == self.from_position
            is_final_position = (intermediate_row, intermediate_col) == self.to_position

            if piece_exists and not is_final_position and not is_initial_position:
                movement_not_blocked = False

        return exists_trajectory and movement_not_blocked

class ComposedMove:
    def __init__(self, moves):
        self.moves = moves

    def do(self):
        for move in self.moves:
            move.do()

    def undo(self):
        for move in self.moves[::-1]:
            move.undo()
        
    def is_valid(self):
        raise NotImplementedError


class Castling(ComposedMove):
    def __init__(self, board, initial_king_position, target_king_position):
        king_initial_row, king_initial_col = initial_king_position
        king_target_row, king_target_col = target_king_position
        
        self.king = board[king_initial_row][king_initial_col]
        self.king_position = initial_king_position
        
        if king_target_col > king_initial_col:
            rook_initial_row, rook_initial_col = king_target_row, king_target_col + 1
            rook_final_row, rook_final_col = king_target_row, king_target_col - 1
        else:
            rook_initial_row, rook_initial_col = king_target_row, king_target_col - 2
            rook_final_row, rook_final_col = king_target_row, king_target_col + 1
        
        self.rook = board[rook_initial_row][rook_initial_col]
        self.rook_position = (rook_initial_row, rook_initial_col)
        final_rook_position = (rook_final_row, rook_final_col)

        self.moves = [
            Movement(board, self.king, self.king_position, target_king_position),
            Movement(board, self.rook, self.rook_position, final_rook_position)
        ]

    def is_valid(self):
        if self.king is None or self.rook is None:
            return False
        if self.king.color != self.rook.color:
            return False
        if self.king.has_moved or self.rook.has_moved:
            return False
        if self.king_position[0] != self.rook_position[0]:
            return False
        return True


class EnPassant(Movement):
    def __init__(self, board, piece, from_position, to_position, captured_piece=None):
        super().__init__(board, piece, from_position, to_position, captured_piece)
        self.previous_move = self.board.history[-1] if self.board.history else None
        self.captured_piece = self.previous_move.piece if self.previous_move is not None else None
        

    def do(self):
        self.board.do_move(
            self.piece,
            self.from_position,
            self.to_position
        )
        capture_position_row, capture_position_col = self.previous_move.to_position
        self.board[capture_position_row][capture_position_col] = None

    def undo(self):
        self.board.do_move(
            self.piece,
            self.to_position,
            self.from_position
        )
        capture_position_row, capture_position_col = self.previous_move.to_position
        self.board[capture_position_row][capture_position_col] = self.captured_piece

    def is_valid(self):
        if not isinstance(self.piece, pieces.Pawn):
            return False

        if not isinstance(self.captured_piece, pieces.Pawn):
            return False

        if self.captured_piece.color == self.piece.color:
            return False

        if not self.previous_move.from_position[1] == self.previous_move.to_position[1]:
            return False
        print("pre", self.previous_move.to_position[0], self.from_position[0])
        if not self.previous_move.to_position[0] == self.from_position[0]:
            return False
        print("falha1")
        if not abs(self.previous_move.to_position[1] - self.from_position[1]) == 1:
            return False
        print("foi")
        return True
