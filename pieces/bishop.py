from .piece import Piece


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'bishop')

    def trajectory(self, from_position, to_position):
        from_row, from_col = from_position
        to_row, to_col = to_position

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

            trajectory = set()
            while (current_row, current_col) != to_position:
                trajectory.add((current_row, current_col))
                current_row += row_tep
                current_col += col_step
            trajectory.add(to_position)

            return trajectory
        return set()
