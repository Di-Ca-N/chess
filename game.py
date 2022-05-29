from pieces import *
from moves import process_move


class ChessGame:
    def __init__(self):
        self.new_game()

    def new_game(self, state_file="initial_position.txt"):
        self.state = {}
        self.player = Colors.WHITE
        self.history = []

        self.piece_dict = {'r': Rook, 'n': Knight, 'k': King, 'q': Queen, 'b': Bishop, 'p': Pawn}

        with open(state_file) as state:
            for r, row in enumerate(state):
                for c, piece_code in enumerate(row):
                    piece_class = self.piece_dict.get(piece_code.lower())
                    if piece_class is None:
                        continue
                    piece_color = Colors.WHITE if piece_code.islower() else Colors.BLACK
                    piece = piece_class(piece_color)
                    self.state[r, c] = piece_class(piece_color)

                    match piece:
                        case King(color=Colors.WHITE):
                            self.white_king_pos = (r, c)
                        case King(color=Colors.BLACK):
                            self.black_king_pos = (r, c)

    def __getitem__(self, position):
        return self.state.get(position)

    def __iter__(self):
        for x in range(8):
            for y in range(8):
                yield (y, x), self.state.get((y, x))

    def process_move(self, from_position, to_position):
        piece = self.state.get(from_position)
        target_piece = self.state.get(to_position)

        return process_move(self, piece, from_position, to_position, target_piece)

    def make_move(self, move):
        if not move.is_valid() or move.piece.color != self.player:
            return

        move.do()
        self.history.append(move)

        king_pos = self.get_king_position(self.player)

        if self.verify_check(king_pos, self.player):
            self.undo_move(keep_player=True)
        else:
            self.change_player()

    def move_piece(self, piece, from_position, to_position):
        self.place_piece(None, from_position)
        self.place_piece(piece, to_position)
        piece.has_moved = True

        # Keeping track of kings' positions for performance reasons
        if isinstance(piece, King):
            if piece.color == Colors.WHITE:
                self.white_king_pos = to_position
            else:
                self.black_king_pos = to_position

    def place_piece(self, piece, position):
        self.state[position] = piece

    def undo_move(self, keep_player=False):
        if not self.history:
            return

        last_move = self.history.pop()
        last_move.undo()
        if not keep_player:
            self.change_player()

    def change_player(self):
        if self.player is Colors.WHITE:
            self.player = Colors.BLACK
        else:
            self.player = Colors.WHITE

    def verify_check(self, position, color):
        for piece_position, piece in self:
            if piece is None or piece.color == color:
                continue
            move = self.process_move(piece_position, position)
            if move is not None and move.is_valid():
                return True
        return False

    def get_king_position(self, player):
        if player == Colors.WHITE:
            return self.white_king_pos
        return self.black_king_pos

if __name__ == "__main__":
    import pprint
    board = ChessGame()
    pprint.pprint(board.state)
