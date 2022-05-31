from .piece import Piece


class Rook(Piece):
    def __init__(self, color, has_moved=False):
        super().__init__(color, "rook", has_moved)
        self.notation = "R"

    def trajectory(self, from_position, to_position, capture=False):
        from_row, from_col = from_position
        to_row, to_col = to_position

        # Rooks can move to any square on the same row or column
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
