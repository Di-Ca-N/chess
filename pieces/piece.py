from abc import ABC, abstractmethod
from .colors import Colors


class Piece(ABC):
    def __init__(self, color: Colors, name: str, has_moved: bool = False):
        self.color = color
        self.name = name
        self.has_moved = has_moved
        self.notation = ""

    def __str__(self):
        return f"{self.color} {self.name}"

    def get_image(self):
        return f'images/{self.color.name.lower()}/{self.name}.png'

    @abstractmethod
    def trajectory(self, from_position, to_position):
        raise NotImplementedError

    def can_capture(self, target_piece, from_position, to_position):
        if target_piece.color == self.color:
            return False

        if self.trajectory(from_position, to_position):
            return True
