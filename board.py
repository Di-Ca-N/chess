from pieces import *
from moves import process_move


class Board:
    def __init__(self):
        self.new_game()

    def new_game(self):
        self.state = {}
        self.player = Colors.WHITE
        self.history = []

        self.state[7, 0] = Rook(Colors.WHITE)
        self.state[7, 1] = Knight(Colors.WHITE)
        self.state[7, 2] = Bishop(Colors.WHITE)
        self.state[7, 3] = Queen(Colors.WHITE)
        self.state[7, 4] = King(Colors.WHITE)
        self.state[7, 5] = Bishop(Colors.WHITE)
        self.state[7, 6] = Knight(Colors.WHITE)
        self.state[7, 7] = Rook(Colors.WHITE)

        for i in range(8):
            self.state[6, i] = Pawn(Colors.WHITE)

        self.state[0, 0] = Rook(Colors.BLACK)
        self.state[0, 1] = Knight(Colors.BLACK)
        self.state[0, 2] = Bishop(Colors.BLACK)
        self.state[0, 3] = Queen(Colors.BLACK)
        self.state[0, 4] = King(Colors.BLACK)
        self.state[0, 5] = Bishop(Colors.BLACK)
        self.state[0, 6] = Knight(Colors.BLACK)
        self.state[0, 7] = Rook(Colors.BLACK) 

        for i in range(8):
            self.state[1, i] = Pawn(Colors.BLACK)

        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)

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
    board = Board()
    pprint.pprint(board.state)
