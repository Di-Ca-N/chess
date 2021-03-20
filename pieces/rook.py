from .piece import Piece


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'rook')

    def trajectory(self, from_position, to_position):
        from_row, from_col = from_position
        to_row, to_col = to_position

        if from_row == to_row:
            if from_col > to_col:
                from_col, to_col = to_col, from_col
            return {(from_row, x) for x in range(from_col, to_col + 1)}

        elif from_col == to_col:
            if from_row > to_row:
                from_row, to_row = to_row, from_row
            return {(x, from_col) for x in range(from_row, to_row + 1)}

        else:
            return set()
