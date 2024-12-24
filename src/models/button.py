# button.py
# Define Button states, colors, positions, etc.
from dataclasses import dataclass

@dataclass
class LaunchpadButton:
    x: int
    y: int
    color: int = 0
    note: int = None

    def __post_init__(self):
        if self.note is None:
            self.note = self.x + (self.y * 10)