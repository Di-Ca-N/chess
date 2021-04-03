from abc import ABC, abstractmethod
from .colors import Colors
import typing

if typing.TYPE_CHECKING:
    from typing import Set, Tuple


class Piece(ABC):
    def __init__(self, color, name, has_moved=False):
        self.color = color
        self.name = name
        self.has_moved = has_moved
        self.notation = ""

    def __str__(self):
        return f"{self.color} {self.name}"

    def get_image(self):
        return f'images/{self.color.name.lower()}/{self.name}.png'

    @abstractmethod
    def trajectory(self, from_position, to_position, capture=False):
        raise NotImplementedError
