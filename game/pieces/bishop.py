from .piece import Piece


class Bishop(Piece):
    def __init__(self, color, has_moved=False):
        super().__init__(color, "bishop", has_moved)
        self.notation = "B"

    def trajectory(self, from_position, to_position, capture=False):
        # Bishops can move to all squares which the sum of its row
        # and col (or the difference between them) is the same of the
        # current position
        from_row, from_col = from_position
        to_row, to_col = to_position

        from_dif = from_row - from_col
        to_dif = to_row - to_col

        from_sum = from_row + from_col
        to_sum = to_row + to_col

        trajectory = set()

        if from_dif == to_dif or from_sum == to_sum:
            row_step = -1 if from_row > to_row else 1
            col_step = -1 if from_col > to_col else 1

            current_row, current_col = from_position

            while (current_row, current_col) != to_position:
                trajectory.add((current_row, current_col))
                current_row += row_step
                current_col += col_step
            trajectory.add(to_position)

        return trajectory
