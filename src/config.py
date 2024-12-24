# config.py
# Put any global configuration values or environment variable loading here.
from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

@dataclass
class Config:
    OBS_HOST: str
    OBS_PORT: int
    OBS_PASSWORD: Optional[str]
    LAUNCHPAD_PORT: str

def load_config() -> Config:
    load_dotenv()
    return Config(
        OBS_HOST=os.getenv('OBS_HOST', 'localhost'),
        OBS_PORT=int(os.getenv('OBS_PORT', '4444')),
        OBS_PASSWORD=os.getenv('OBS_PASSWORD'),
        LAUNCHPAD_PORT=os.getenv('LAUNCHPAD_PORT', 'Launchpad Mini MK3 LPMiniMK3 MIDI In')
    )