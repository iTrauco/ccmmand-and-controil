import logging
from src.config import load_config
from src.controllers.launchpad import LaunchpadController
from src.controllers.obs import OBSController
from src.services.mapping_service import MappingService
from src.utils.logger import setup_logger
from src.services.alias_service import AliasService

logger = setup_logger()

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
    
    # Initialize services (only once!)
    alias_service = AliasService()
    mapping_service = MappingService(obs_controller=obs, alias_service=alias_service)

    # Scene controls (top row)
    scene_mappings = [
        ("Scene 1", 0, 0),
        ("Scene 2", 1, 0),
        ("Scene 3", 2, 0),
    ]

    # Source toggles (second row)
    source_mappings = [
        ("Webcam", 0, 1),
        ("Microphone", 1, 1),
        ("Screen Share", 2, 1),
    ]

    # Register all mappings
    for scene_name, x, y in scene_mappings:
        button = mapping_service.map_scene(x, y, scene_name)
        launchpad.register_callback(button, mapping_service.get_action(x, y).callback)

    for source_name, x, y in source_mappings:
        button = mapping_service.map_source_toggle(x, y, source_name)
        launchpad.register_callback(button, mapping_service.get_action(x, y).callback)

    # Add alias button (third row)
    alias_button = mapping_service.map_alias_trigger(4, 4, "claude1")  # Changed coordinates to (4,4)
    launchpad.register_callback(alias_button, mapping_service.get_action(4, 4).callback)

    logger.info("Launchpad OBS Controller started")
    logger.info("Top row (Green): Scene switching")
    logger.info("Second row (Yellow): Source toggling")
    logger.info("Third row (Blue): Alias triggers")
    logger.info("Press Ctrl+C to exit")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Shutting down...")

if __name__ == "__main__":
    main()