from .piece import Piece


class King(Piece):
    def __init__(self, color, has_moved=False):
        super().__init__(color, 'king', has_moved)
        self.notation = "K"

    def trajectory(self, from_position, to_position, capture=False):
        from_row, from_col = from_position
        to_row, to_col = to_position

        trajectory = set()

        if from_row == to_row:
            if from_col > to_col:
                from_col, to_col = to_col, from_col
            trajectory = {(from_row, x) for x in range(from_col, to_col + 1)}

        elif from_col == to_col:
            if from_row > to_row:
                from_row, to_row = to_row, from_row
            trajectory = {(x, from_col) for x in range(from_row, to_row + 1)}
        else:
            from_dif = from_row - from_col
            to_dif = to_row - to_col

            from_sum = from_row + from_col
            to_sum = to_row + to_col

            if from_dif == to_dif or from_sum == to_sum:
                if from_row > to_row:
                    row_tep = -1
                else:
                    row_tep = 1

                if from_col > to_col:
                    col_step = -1
                else:
                    col_step = 1

                current_row, current_col = from_position

                while (current_row, current_col) != to_position:
                    trajectory.add((current_row, current_col))
                    current_row += row_tep
                    current_col += col_step
                trajectory.add(to_position)

        if len(trajectory) == 2:
            return trajectory
        return set()
