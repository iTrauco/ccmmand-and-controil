# mapping_service.py
# Maps buttons to actions or scenes.
from typing import Dict, Optional
from ..models.button import LaunchpadButton
from ..models.action import Action, ActionType
from ..controllers.obs import OBSController
from ..utils.constants import Colors

class MappingService:
    def __init__(self, obs_controller: OBSController):
        self.obs = obs_controller
        self.mappings: Dict[tuple, Action] = {}

    def map_scene(self, x: int, y: int, scene_name: str) -> LaunchpadButton:
        button = LaunchpadButton(x, y, Colors.GREEN)
        action = Action(
            type=ActionType.SCENE_CHANGE,
            payload=scene_name,
            callback=lambda: self.obs.switch_scene(scene_name)
        )
        self.mappings[(x, y)] = action
        return button

    def map_source_toggle(self, x: int, y: int, source_name: str) -> LaunchpadButton:
        button = LaunchpadButton(x, y, Colors.YELLOW)
        action = Action(
            type=ActionType.SOURCE_TOGGLE,
            payload=source_name,
            callback=lambda: self.obs.toggle_source_visibility(source_name)
        )
        self.mappings[(x, y)] = action
        return button

    def get_action(self, x: int, y: int) -> Optional[Action]:
        return self.mappings.get((x, y))