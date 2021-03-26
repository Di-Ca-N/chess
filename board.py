from pieces import *
from moves import process_move


class Board:
    def __init__(self):
        self.new_game()

    def new_game(self):
        self.state = [[None for _ in range(8)] for _ in range(8)]
        self.player = Colors.WHITE
        self.history = []

        self.state[7][0] = Rook(Colors.WHITE)
        self.state[7][1] = Knight(Colors.WHITE)
        self.state[7][2] = Bishop(Colors.WHITE)
        self.state[7][3] = Queen(Colors.WHITE)
        self.state[7][4] = King(Colors.WHITE)
        self.state[7][5] = Bishop(Colors.WHITE)
        self.state[7][6] = Knight(Colors.WHITE)
        self.state[7][7] = Rook(Colors.WHITE)

        for i in range(8):
            self.state[6][i] = Pawn(Colors.WHITE)

        self.state[0][0] = Rook(Colors.BLACK)
        self.state[0][1] = Knight(Colors.BLACK)
        self.state[0][2] = Bishop(Colors.BLACK)
        self.state[0][3] = Queen(Colors.BLACK)
        self.state[0][4] = King(Colors.BLACK)
        self.state[0][5] = Bishop(Colors.BLACK)
        self.state[0][6] = Knight(Colors.BLACK)
        self.state[0][7] = Rook(Colors.BLACK)

        for i in range(8):
            self.state[1][i] = Pawn(Colors.BLACK)

    def __getitem__(self, position):
        return self.state[position]

    def process_move(self, from_position, to_position):
        from_row, from_col = from_position
        to_row, to_col = to_position

        piece = self.state[from_row][from_col]

        if piece is None:
            return

        if piece.color != self.player:
            return

        target_piece = self.state[to_row][to_col]

        move = process_move(self, piece, from_position, to_position, target_piece)
        return move

    def make_move(self, move):
        if move is not None and move.is_valid():
            move.do()
            self.history.append(move)
            self.change_player()

    def move_piece(self, piece, from_position, to_position):
        from_row, from_col = from_position
        to_row, to_col = to_position
        self.state[from_row][from_col] = None
        self.state[to_row][to_col] = piece
        piece.has_moved = True

    def undo_move(self):
        if self.history:
            last_move = self.history.pop()
            last_move.undo()
            self.change_player()

    def change_player(self):
        if self.player is Colors.WHITE:
            self.player = Colors.BLACK
        else:
            self.player = Colors.WHITE



if __name__ == "__main__":
    import pprint
    board = Board()
    pprint.pprint(board.state)
