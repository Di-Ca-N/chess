from abc import ABC, abstractmethod
import enum
from typing import TypeAlias

Position: TypeAlias = tuple[int, int]


class Color(enum.Enum):
    WHITE = -1
    BLACK = 1


class Piece(ABC):
    """Abstract class to represent a piece

    Subclasses must implement the method 'trajectory'

    Attributes:
        color (Color): Color of the piece
        name (str): Name of the piece. Used to find the piece assets
        has_moved (bool): Indicate whether the piece have already moved
                          in the current game. Default is False
        notation (str): Text notation of the piece. In general, it is
                        only one letter
    """

    def __init__(self, color: Color, name: str, has_moved: bool = False):
        self.color = color
        self.name = name
        self.has_moved = has_moved

    def __str__(self):
        return f"{self.color} {self.name}"

    def get_image_path(self) -> str:
        """Return the path to the image associated with this piece"""
        return f"assets/images/{self.color.name.lower()}/{self.name}.png"

    @abstractmethod
    def trajectory(
        self, from_position: Position, to_position: Position, capture: bool = False
    ) -> set:
        """Find the trajectory between 'from_position' and 'to_position',
        according to the piece movement restrictions and rules.

        This is an abstract method and must be overwritten by all
        subclasses.

        Arguments:
            from_position (tuple[int, int]): Initial position
            to_position (tuple[int, int]): Target position
            capture (bool): Indicate if the move is a capture or not.
                            Default to False
        """
        raise NotImplementedError


def diagonal_trajectory(origin, target):
    # A diagonal movement happen when the sum or difference of the
    # coordinates of the origin and target position are equal
    from_dif = origin[0] - origin[1]
    to_dif = target[0] - target[1]

    from_sum = origin[0] + origin[1]
    to_sum = target[0] + target[1]

    trajectory = set()

    if from_dif == to_dif or from_sum == to_sum:
        row_step = -1 if origin[0] > target[0] else 1
        col_step = -1 if origin[1] > target[1] else 1

        current_row, current_col = origin

        while (current_row, current_col) != target:
            trajectory.add((current_row, current_col))
            current_row += row_step
            current_col += col_step
        trajectory.add(target)

    return trajectory


def straight_trajectory(origin, target):
    from_row, from_col = origin
    to_row, to_col = target

    # Queens can move to any square on the same row or column (like Rooks)
    if from_row == to_row:
        if from_col > to_col:
            from_col, to_col = to_col, from_col
        return {(from_row, x) for x in range(from_col, to_col + 1)}

    elif from_col == to_col:
        if from_row > to_row:
            from_row, to_row = to_row, from_row
        return {(x, from_col) for x in range(from_row, to_row + 1)}
    return set()


class King(Piece):
    def __init__(self, color, has_moved=False):
        super().__init__(color, "king", has_moved)

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


class Queen(Piece):
    def __init__(self, color, has_moved=False):
        super().__init__(color, "queen", has_moved)

    def trajectory(self, from_position, to_position, capture=False):
        if trajectory := straight_trajectory(from_position, to_position):
            return trajectory

        return diagonal_trajectory(from_position, to_position)


class Bishop(Piece):
    def __init__(self, color, has_moved=False):
        super().__init__(color, "bishop", has_moved)

    def trajectory(self, from_position, to_position, capture=False):
        return diagonal_trajectory(from_position, to_position)


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


class Rook(Piece):
    def __init__(self, color, has_moved=False):
        super().__init__(color, "rook", has_moved)

    def trajectory(self, from_position, to_position, capture=False):
        return straight_trajectory(from_position, to_position)


class Pawn(Piece):
    def __init__(self, color, has_moved=False):
        super().__init__(color, "pawn", has_moved)

    def trajectory(self, from_position, to_position, capture=False):
        from_row, from_col = from_position
        to_row, to_col = to_position

        trajectory = set()
        if not capture:
            # If not capturing, a pawn can only move to the same column
            if from_col == to_col:
                limit = 2 if not self.has_moved else 1

                if abs(to_row - from_row) <= limit:
                    if self.color == Color.WHITE:
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
