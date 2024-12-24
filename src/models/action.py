from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

class ActionType(Enum):
    SCENE_CHANGE = "scene_change"
    SOURCE_TOGGLE = "source_toggle"
    CUSTOM = "custom"

@dataclass
class Action:
    type: ActionType
    payload: Any
    callback: Callable