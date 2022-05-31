from .piece import Piece, Colors


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "pawn")
        self.notation = ""

    def trajectory(self, from_position, to_position, capture=False):
        from_row, from_col = from_position
        to_row, to_col = to_position

        trajectory = set()
        if not capture:
            # If not capturing, a pawn can only move to the same column
            if from_col == to_col:
                limit = 2 if not self.has_moved else 1

                if abs(to_row - from_row) <= limit:
                    if self.color == Colors.WHITE:
                        trajectory = {
                            (x, from_col) for x in range(to_row, from_row + 1)
                        }
                    else:
                        trajectory = {
                            (x, from_col) for x in range(from_row, to_row + 1)
                        }
        else:
            # If capturing, it can move forward one square and one
            # column to the side
            if to_row - from_row == self.color.value and abs(from_col - to_col) == 1:
                trajectory = {from_position, to_position}

        return trajectory
