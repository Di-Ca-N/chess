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

    def __init__(
        self, color: Color, name: str, has_moved: bool = False
    ):
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
