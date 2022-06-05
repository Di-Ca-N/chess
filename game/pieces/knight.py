from .piece import Piece


class Knight(Piece):
    def __init__(self, color, has_moved=False):
        super().__init__(color, "knight", has_moved)

    def trajectory(self, from_position, to_position, capture=False):
        from_row, from_col = from_position
        to_row, to_col = to_position

        # Knights can jump two squares in one direction and 1 square the
        # other direction, doesn't matter the orientation
        diff = (abs(to_row - from_row), abs(to_col - from_col))
        if diff in {(1, 2), (2, 1)}:
            return {from_position, to_position}
        else:
            return set()
