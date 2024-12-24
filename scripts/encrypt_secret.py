from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.secrets import SecretsManager
from dotenv import load_dotenv
import os

def encrypt_secrets():
    """Encrypt sensitive values and update .env file"""
    load_dotenv()
    secrets = SecretsManager()
    
    # Read current .env file
    env_path = Path('.env')
    if not env_path.exists():
        print("No .env file found. Creating from .env.example...")
        with open('.env.example', 'r') as example:
            with open('.env', 'w') as env:
                env.write(example.read())
    
    # Get password from user
    password = input("Enter OBS WebSocket password (press Enter if none): ").strip()
    
    if password:
        encrypted_password = secrets.encrypt(password)
        
        # Update .env file
        env_contents = []
        password_updated = False
        
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('OBS_PASSWORD='):
                    env_contents.append(f'OBS_PASSWORD={encrypted_password}\n')
                    password_updated = True
                else:
                    env_contents.append(line)
                    
        if not password_updated:
            env_contents.append(f'OBS_PASSWORD={encrypted_password}\n')
            
        with open('.env', 'w') as f:
            f.writelines(env_contents)
            
        print("Password encrypted and saved to .env")
    else:
        print("No password provided. Skipping encryption.")

if __name__ == "__main__":
    encrypt_secrets()