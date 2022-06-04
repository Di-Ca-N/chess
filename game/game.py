from itertools import product
from .pieces import *
from .moves import process_move


class ChessGame:
    """Implements the core logic and interactions of the Chess game"""

    def __init__(self):
        self.new_game()

    def new_game(self, state_file="assets/initial_position.txt"):
        """Starts a new game with the given initial state

        The state should be the path to a text file with 8 rows and 8
        columns, with each character representing a piece.

        Arguments:
            state_file (str): path to the state file

        ToDo:
            - Change API to receive an iterable instead of a path to a
            file
        """

        self.state = {}
        self.player = Color.WHITE
        self.history = []
        self.game_over = False
        self.winner = None

        self.piece_dict = {
            "r": Rook,
            "n": Knight,
            "k": King,
            "q": Queen,
            "b": Bishop,
            "p": Pawn,
        }

        # Loads the initial state file
        with open(state_file) as state:
            for r, row in enumerate(state):
                for c, piece_code in enumerate(row):
                    piece_class = self.piece_dict.get(piece_code.lower())
                    if piece_class is None:
                        continue
                    piece_color = Color.WHITE if piece_code.islower() else Color.BLACK
                    piece = piece_class(piece_color)
                    self.state[r, c] = piece_class(piece_color)

                    # Save king positions to allow for efficient detection of checks
                    match piece:
                        case King(color=Color.WHITE):
                            self.white_king_pos = (r, c)
                        case King(color=Color.BLACK):
                            self.black_king_pos = (r, c)

    def __getitem__(self, position):
        return self.state.get(position)

    def __iter__(self):
        for x in range(8):
            for y in range(8):
                yield (y, x), self.state.get((y, x))

    def process_move(self, from_position, to_position):
        """Returns a Movement instance that moves a piece from the first position to the second

        Arguments:
            from_position (tuple[int, int]): Original piece position
            to_position (tuple[int, int]): Target piece position
        """

        piece = self.state.get(from_position)
        target_piece = self.state.get(to_position)

        return process_move(self, piece, from_position, to_position, target_piece)

    def make_move(self, move):
        """Make a movement, if it is valid

        Arguments:
            move (Movement): Movement to be executed
        """

        if self.game_over:
            return

        # Invalid moves or from the wrong player are not processed
        if not move.is_valid() or move.piece.color != self.player:
            return

        move.do()
        self.history.append(move)

        # If the player's king is in check after the movement, undo it
        king_pos = self._get_king_position(self.player)
        if self.verify_check(king_pos, self.player):
            self.undo_move(swap_player=False)
        else:
            last_player = self.player
            self._change_player()

            if self.verify_checkmate(self.player):
                self.winner = last_player
                self.game_over = True

    def undo_move(self, swap_player=True):
        """Undo the last move.

        Swaps players if the 'swap_player' flag is given

        Arguments:
            swap_player (bool): Control whether to swap players after
                the movement is undone.
        """

        # Cannot undo moves if the history is empty
        if not self.history:
            return

        last_move = self.history.pop()
        last_move.undo()

        if swap_player:
            self._change_player()

    def move_piece(self, piece, from_position, to_position):
        """Moves a piece from position one position to another

        This method is meant to be called only by Movement instances,
        while they are executing. When called, the 'from_position' is
        set to None and the given piece is placed in 'to_position',
        regardless of what is on any of the positions. This method
        performs no validation of the applied movements

        Arguments:
            piece (Piece): piece to place in the 'to_position'
            from_position (tuple[int, int]): Position to set to None
            to_position (tuple[int, int]): Position to place the piece
        """
        self.place_piece(None, from_position)
        self.place_piece(piece, to_position)
        piece.has_moved = True

        # Keeping track of kings' positions for performance reasons
        if isinstance(piece, King):
            if piece.color == Color.WHITE:
                self.white_king_pos = to_position
            else:
                self.black_king_pos = to_position

    def place_piece(self, piece, position):
        self.state[position] = piece

    def _change_player(self):
        """Swap the current player"""

        if self.player is Color.WHITE:
            self.player = Color.BLACK
        else:
            self.player = Color.WHITE

    def verify_check(self, position, color):
        """Check if the a position is being attacked by the opponent

        Arguments:
            position (tuple[int, int]): Position to check for attacks
            color (Color): allied color
        """
        for piece_position, piece in self:
            # Ignore empty squares and allied pieces
            if piece is None or piece.color == color:
                continue

            move = self.process_move(piece_position, position)
            if move.is_valid():
                return True
        return False

    def verify_checkmate(self, color):
        """Verify if the game ended in checkmate
        
        Arguments:
            color (Color): color to check if was checkmated
        """
        enemy_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        checkmate = True
        for piece_position, piece in self:
            if piece is None or piece.color == enemy_color:
                continue
    
            for target_position in product(range(8), repeat=2):
                move = self.process_move(piece_position, target_position)
                if not move.is_valid():
                    continue
                
                move.do()
                king_position = self._get_king_position(color)
                if not self.verify_check(king_position, color):
                    checkmate = False
                move.undo()

                if not checkmate:
                    break
            if not checkmate:
                break
        return checkmate

    def _get_king_position(self, player):
        """Return the king position of the requested player

        Arguments:
            player (Colors): Color of the king
        """
        if player == Color.WHITE:
            return self.white_king_pos
        return self.black_king_pos
