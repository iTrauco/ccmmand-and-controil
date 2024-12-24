import logging
from src.config import load_config
from src.controllers.launchpad import LaunchpadController
from src.controllers.obs import OBSController
from src.models.button import LaunchpadButton
from src.utils.constants import Colors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load configuration
    config = load_config()

    # Initialize controllers
    try:
        launchpad = LaunchpadController(config.LAUNCHPAD_PORT)
        obs = OBSController(config.OBS_HOST, config.OBS_PORT, config.OBS_PASSWORD)
    except Exception as e:
        logger.error(f"Failed to initialize controllers: {e}")
        return

    # Example mapping: Switch to "Scene 1" when pressing pad at (0,0)
    scene1_button = LaunchpadButton(0, 0, Colors.GREEN)
    launchpad.register_callback(
        scene1_button,
        lambda: obs.switch_scene("Scene 1")
    )

    logger.info("Launchpad OBS Controller started. Press Ctrl+C to exit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Shutting down...")

if __name__ == "__main__":
    main()