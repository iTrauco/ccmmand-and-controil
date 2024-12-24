# obs.py
# OBS WebSocket control logic goes here.
from obswebsocket import obsws, requests
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class OBSController:
    def __init__(self, host: str, port: int, password: Optional[str] = None):
        self.ws = obsws(host, port, password)
        try:
            self.ws.connect()
            logger.info("Connected to OBS WebSocket")
        except Exception as e:
            logger.error(f"Failed to connect to OBS: {e}")
            raise

    def switch_scene(self, scene_name: str):
        try:
            self.ws.call(requests.SetCurrentScene(scene_name))
            logger.info(f"Switched to scene: {scene_name}")
        except Exception as e:
            logger.error(f"Failed to switch scene: {e}")