from abc import ABC, abstractmethod
import enum


class Colors(enum.Enum):
    WHITE = -1
    BLACK = 1


class Piece(ABC):
    def __init__(self, color, name, has_moved=False):
        self.color = color
        self.name = name
        self.has_moved = has_moved
        self.notation = ""

    def __str__(self):
        return f"{self.color} {self.name}"

    def get_image(self):
        return f"assets/images/{self.color.name.lower()}/{self.name}.png"

    @abstractmethod
    def trajectory(self, from_position, to_position, capture=False):
        raise NotImplementedError
