# src/config.py
from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv
from .utils.secrets import SecretsManager
import logging

logger = logging.getLogger(__name__)

@dataclass
class Config:
    OBS_HOST: str
    OBS_PORT: int
    OBS_PASSWORD: Optional[str]
    LAUNCHPAD_PORT: str

def load_config() -> Config:
    load_dotenv('secrets.env')
    secrets = SecretsManager()
    
    # Get encrypted password and log all connection details
    encrypted_password = os.getenv('OBS_PASSWORD')
    decrypted_password = secrets.decrypt(encrypted_password) if encrypted_password else None
    
    print("DEBUG Connection Details:")
    print(f"Host: {os.getenv('OBS_HOST')}")
    print(f"Port: {os.getenv('OBS_PORT')}")
    # print(f"Decrypted Password: {decrypted_password}")

    return Config(
        OBS_HOST=os.getenv('OBS_HOST', 'localhost'),
        OBS_PORT=int(os.getenv('OBS_PORT', '4444')),
        OBS_PASSWORD=decrypted_password,
        LAUNCHPAD_PORT=os.getenv('LAUNCHPAD_PORT', 'Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 20:1')
    )