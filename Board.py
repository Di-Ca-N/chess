from pieces import *
from moves.Movement import Movement


class Board:
    def __init__(self):
        self.state = [[None for i in range(8)] for j in range(8)]
        self.player = Colors.WHITE
        self.historic = []

    def new_game(self):
        self.state = [[None for i in range(8)] for j in range(8)]
        self.player = Colors.WHITE
        self.historic = []

        self.state[7][0] = Tower(Colors.WHITE)
        self.state[7][1] = Horse(Colors.WHITE)
        self.state[7][2] = Bishop(Colors.WHITE)
        self.state[7][3] = Queen(Colors.WHITE)
        self.state[7][4] = King(Colors.WHITE)
        self.state[7][5] = Bishop(Colors.WHITE)
        self.state[7][6] = Horse(Colors.WHITE)
        self.state[7][7] = Tower(Colors.WHITE)

        for i in range(8):
            self.state[6][i] = Pawn(Colors.WHITE)

        self.state[0][0] = Tower(Colors.BLACK)
        self.state[0][1] = Horse(Colors.BLACK)
        self.state[0][2] = Bishop(Colors.BLACK)
        self.state[0][3] = Queen(Colors.BLACK)
        self.state[0][4] = King(Colors.BLACK)
        self.state[0][5] = Bishop(Colors.BLACK)
        self.state[0][6] = Horse(Colors.BLACK)
        self.state[0][7] = Tower(Colors.BLACK)

        for i in range(8):
            self.state[1][i] = Pawn(Colors.BLACK)

    def __getitem__(self, position):
        return self.state[position]

    def move_piece(self, from_position, to_position):
        from_row, from_col = from_position
        to_row, to_col = to_position

        piece = self.state[from_row][from_col]

        if piece is None:
            return

        if piece.color != self.player:
            return

        target_piece = self.state[to_row][to_col]

        movement_done = False
        possible = False

        if self.validate_movement(piece, from_position, to_position):
            if target_piece is None:
                possible = True

            else:
                possible = self.validate_capture(piece, target_piece, from_position, to_position)

        if possible:
            self.do_move(piece, from_position, to_position)
            self.historic.append(
                Movement(piece, from_position,
                            to_position, True, target_piece)
            )
            movement_done = True

        if movement_done:
            self.change_player()

    def do_move(self, piece, from_position, to_position):
        from_row, from_col = from_position
        to_row, to_col = to_position
        self.state[from_row][from_col] = None
        self.state[to_row][to_col] = piece
        piece.has_moved = True

    def change_player(self):
        if self.player is Colors.WHITE:
            self.player = Colors.BLACK
        else:
            self.player = Colors.WHITE

    def validate_movement(self, piece, from_position, to_position):
        if piece is None:
            return False

        movement_not_blocked = True
        exists_trajectory = True

        trajectory = piece.trajectory(from_position, to_position)
        if not trajectory:
            exists_trajectory = False

        for intermediate_row, intermediate_col in trajectory:
            intermediary_square = self.state[intermediate_row][intermediate_col]

            piece_exists = intermediary_square is not None
            is_initial_position = (intermediate_row, intermediate_col) == from_position
            is_final_position = (intermediate_row, intermediate_col) == to_position

            if piece_exists and not is_final_position and not is_initial_position:
                movement_not_blocked = False

        return exists_trajectory and movement_not_blocked

    def validate_capture(self, piece, target_piece, from_position, to_position):
        return piece.can_capture(target_piece, from_position, to_position)

    def undo(self):
        if self.historic:
            last_move = self.historic.pop()
            last_move.undo(self)
            self.change_player()


if __name__ == "__main__":
    import pprint
    board = Board()
    pprint.pprint(board.state)
