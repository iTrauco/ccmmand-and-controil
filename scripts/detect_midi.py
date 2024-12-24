import rtmidi
from typing import Dict, List
import sys
from pathlib import Path

# Add project root to path so we can import from src
sys.path.append(str(Path(__file__).parent.parent))
from src.utils.logger import setup_logger

logger = setup_logger()

class MIDIDetector:
    def __init__(self):
        self.midi_in = rtmidi.MidiIn()
        self.midi_out = rtmidi.MidiOut()

    def get_ports(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Returns a dictionary of available MIDI ports
        """
        return {
            "inputs": {"available": self.midi_in.get_ports()},
            "outputs": {"available": self.midi_out.get_ports()}
        }

    def print_ports(self) -> None:
        """
        Prints available MIDI ports in a formatted way
        """
        ports = self.get_ports()
        
        print("\n=== Available MIDI Ports ===")
        print("\nInput Ports:")
        if ports["inputs"]["available"]:
            for i, port in enumerate(ports["inputs"]["available"]):
                print(f"{i}: {port}")
        else:
            print("No input ports available")

        print("\nOutput Ports:")
        if ports["outputs"]["available"]:
            for i, port in enumerate(ports["outputs"]["available"]):
                print(f"{i}: {port}")
        else:
            print("No output ports available")

        # Look specifically for Launchpad
        launchpad_ports = [
            port for port in ports["inputs"]["available"] 
            if "launchpad" in port.lower()
        ]
        
        if launchpad_ports:
            print("\n=== Detected Launchpad Devices ===")
            for port in launchpad_ports:
                print(f"Found Launchpad: {port}")
                print(f"Add this to your .env file as: LAUNCHPAD_PORT={port}")

def main():
    try:
        detector = MIDIDetector()
        detector.print_ports()
    except Exception as e:
        logger.error(f"Error detecting MIDI ports: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()