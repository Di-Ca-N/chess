from abc import ABC, abstractmethod
from .colors import Colors
import typing

if typing.TYPE_CHECKING:
    from typing import Set, Tuple


class Piece(ABC):
    def __init__(self, color: Colors, name: str, has_moved: bool = False):
        self.color = color
        self.name = name
        self.has_moved = has_moved
        self.notation = ""

    def __str__(self) -> str:
        return f"{self.color} {self.name}"

    def get_image(self) -> str:
        return f'images/{self.color.name.lower()}/{self.name}.png'

    @abstractmethod
    def trajectory(self, from_position: 'Tuple[int, int]', to_position: 'Tuple[int, int]') -> 'Set[Tuple[int, int]]':
        raise NotImplementedError

    def can_capture(self, target_piece: 'Piece', from_position: 'Tuple[int, int]', to_position: 'Tuple[int, int]') -> bool:
        if target_piece.color == self.color:
            return False

        if self.trajectory(from_position, to_position):
            return True
