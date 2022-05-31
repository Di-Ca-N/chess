from .piece import Piece


class King(Piece):
    def __init__(self, color, has_moved=False):
        super().__init__(color, "king", has_moved, "K")

    def trajectory(self, from_position, to_position, capture=False):
        from_row, from_col = from_position
        to_row, to_col = to_position

        # Kings can move to any adjacent square
        row_dif = abs(from_row - to_row)
        col_dif = abs(from_col - to_col)

        if row_dif <= 1 and col_dif <= 1:
            return {from_position, to_position}
        else:
            return set()
