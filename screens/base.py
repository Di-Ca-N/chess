from dataclasses import dataclass, field


@dataclass
class ScreenTransition:
    from_state: str
    to_state: str
    data: dict = field(default_factory=dict)


class Screen:
    def __init__(self):
        self.transition = None

    def draw(self, surface):
        pass

    def handle_event(self, event):
        pass

    def get_transition(self):
        return self.transition
