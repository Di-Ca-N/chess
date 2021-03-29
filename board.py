from pieces import *
from moves import process_move, Movement, ComposedMove
from typing import Tuple, Union


Position = Tuple[int, int]

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
        
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)

    def __getitem__(self, position: int):
        return self.state[position]

    def process_move(self, from_position: Position, to_position: Position):
        from_row, from_col = from_position
        to_row, to_col = to_position

        piece = self.state[from_row][from_col]
        target_piece = self.state[to_row][to_col]

        move = process_move(self, piece, from_position, to_position, target_piece)
        return move

    def make_move(self, move: Union[Movement, ComposedMove]):
        if move is None or not move.is_valid() or move.piece.color != self.player:
            return
        move.do()
        self.history.append(move)

        king_pos = self.get_king_position(self.player)

        if self.verify_check(king_pos, self.player):
            self.undo_move(keep_player=True)
        else:
            self.change_player()
    
    def move_piece(self, piece: Piece, from_position: Position, to_position: Position):
        from_row, from_col = from_position
        to_row, to_col = to_position
        self.state[from_row][from_col] = None
        self.state[to_row][to_col] = piece    
        piece.has_moved = True

        # Keeping track of kings' positions for performance reasons
        if isinstance(piece, King):
            if piece.color == Colors.WHITE:
                self.white_king_pos = to_position
            else:
                self.black_king_pos = to_position

    def undo_move(self, keep_player=False):
        if self.history:
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
        for row_n, row in enumerate(self.state):
            for col_n, piece in enumerate(row):
                if piece is not None and piece.color != color:
                    move = self.process_move((row_n, col_n), position)
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
