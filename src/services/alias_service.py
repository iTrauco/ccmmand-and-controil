# Path: src/services/alias_service.py
import os
import subprocess
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class AliasService:
    def __init__(self):
        self.home = str(Path.home())
        self.rc_file = os.path.join(self.home, '.zshrc')
        
    # Path: src/services/alias_service.py
    # Path: src/services/alias_service.py
    # Path: src/services/alias_service.py
    def execute_alias(self, alias_name: str):
        try:
            # Use zsh in login mode to ensure all configs are loaded
            command = f"zsh -i -c '{alias_name}'"
            
            logger.info(f"Executing command: {command}")
            
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                executable='/bin/zsh',
                env=os.environ.copy(),
                start_new_session=True
            )
            
            stdout, stderr = process.communicate()
            if stdout:
                logger.info(f"Command output: {stdout.decode()}")
            if stderr:
                logger.error(f"Command error: {stderr.decode()}")
                
            return True
                
        except Exception as e:
            logger.error(f"Failed to execute alias {alias_name}: {e}")
            return False