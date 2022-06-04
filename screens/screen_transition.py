from dataclasses import dataclass, field


@dataclass
class ScreenTransition:
    from_state: str
    to_state: str
    data: dict = field(default_factory=dict)
