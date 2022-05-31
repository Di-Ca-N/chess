from .piece import Piece


class Queen(Piece):
    def __init__(self, color, has_moved=False):
        super().__init__(color, "queen", has_moved)
        self.notation = "Q"

    def trajectory(self, from_position, to_position, capture=False):
        from_row, from_col = from_position
        to_row, to_col = to_position

        # Queens can move to any square on the same row or column (like Rooks)
        if from_row == to_row:
            if from_col > to_col:
                from_col, to_col = to_col, from_col
            return {(from_row, x) for x in range(from_col, to_col + 1)}

        elif from_col == to_col:
            if from_row > to_row:
                from_row, to_row = to_row, from_row
            return {(x, from_col) for x in range(from_row, to_row + 1)}

        # And also in diagonals (like bishops)
        from_dif = from_row - from_col
        to_dif = to_row - to_col

        from_sum = from_row + from_col
        to_sum = to_row + to_col

        if from_dif == to_dif or from_sum == to_sum:
            row_step = -1 if from_row > to_row else 1
            col_step = -1 if from_col > to_col else 1

            current_row, current_col = from_position

            trajectory = set()
            while (current_row, current_col) != to_position:
                trajectory.add((current_row, current_col))
                current_row += row_step
                current_col += col_step
            trajectory.add(to_position)

            return trajectory
        return set()
