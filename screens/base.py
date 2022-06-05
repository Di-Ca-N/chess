from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class ScreenTransition:
    from_state: str
    to_state: str
    data: dict = field(default_factory=dict)


class Screen(ABC):
    def __init__(self):
        self.transition = None

    @abstractmethod
    def draw(self, surface):
        raise NotImplementedError

    @abstractmethod
    def handle_event(self, event):
        raise NotImplementedError

    def get_transition(self):
        return self.transition
