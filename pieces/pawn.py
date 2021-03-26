from .piece import Piece
from .colors import Colors


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'pawn')

    def trajectory(self, from_position, to_position):
        from_row, from_col = from_position
        to_row, to_col = to_position

        trajectory = {}
        if from_col == to_col:
            limit = 2 if not self.has_moved else 1

            if abs(to_row - from_row) <= limit:
                if self.color == Colors.WHITE:
                    trajectory = {(x, from_col)
                                  for x in range(to_row, from_row + 1)}
                else:
                    trajectory = {(x, from_col)
                                  for x in range(from_row, to_row + 1)}

        return trajectory

    def can_capture(self, target_piece, from_position, to_position):
        from_row, from_col = from_position
        to_row, to_col = to_position

        possible = (to_row - from_row == self.color.value and to_col - from_col in {-1, 1})

        return possible and target_piece.color != self.color
