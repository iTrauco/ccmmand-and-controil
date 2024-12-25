# launchpad.py
# MIDI control logic goes here.
import rtmidi
from typing import Callable, Dict
import logging
from ..models.button import LaunchpadButton
from ..utils.constants import MIDI_NOTE_ON, Colors
import random
import time
import threading

logger = logging.getLogger(__name__)

class LaunchpadController:
    def __init__(self, port_name: str):
        self.midi_in = rtmidi.MidiIn()
        self.midi_out = rtmidi.MidiOut()
        self.callbacks: Dict[int, Callable] = {}
        self.dynamic_buttons: Dict[int, bool] = {}  # Track which buttons should cycle colors
        self._connect_ports(port_name)
        self._start_color_cycle_thread()

    def _connect_ports(self, port_name: str):
        in_ports = self.midi_in.get_ports()
        out_ports = self.midi_out.get_ports()
        
        try:
            in_port = in_ports.index(port_name)
            out_port = out_ports.index(port_name)
            self.midi_in.open_port(in_port)
            self.midi_out.open_port(out_port)
            self.midi_in.set_callback(self._midi_callback)
            logger.info(f"Connected to Launchpad on port: {port_name}")
        except ValueError:
            logger.error(f"Could not find Launchpad port: {port_name}")
            raise

    def _midi_callback(self, event, _):
        message, _ = event
        if len(message) == 3:  # Note messages are 3 bytes
            note = message[1]
            velocity = message[2]
            if velocity > 0 and note in self.callbacks:
                self.callbacks[note]()

    def set_button_color(self, button: LaunchpadButton):
        self.midi_out.send_message([MIDI_NOTE_ON, button.note, button.color])

    def register_callback(self, button: LaunchpadButton, callback: Callable):
        self.callbacks[button.note] = callback
        self.set_button_color(button)  # Set initial color


    def _start_color_cycle_thread(self):
        def cycle_colors():
            while True:
                for note, should_cycle in self.dynamic_buttons.items():
                    if should_cycle:
                        # Choose a random vibrant color
                        color = random.choice([
                            Colors.RED,
                            Colors.GREEN,
                            Colors.YELLOW,
                            Colors.BLUE
                        ])
                        self.midi_out.send_message([MIDI_NOTE_ON, note, color])
                time.sleep(0.5)  # Adjust timing of color changes

        self.color_thread = threading.Thread(target=cycle_colors, daemon=True)
        self.color_thread.start()

    def set_dynamic_button(self, button: LaunchpadButton, is_dynamic: bool = True):
        self.dynamic_buttons[button.note] = is_dynamic
        if not is_dynamic:
            self.set_button_color(button)  # Reset to original color if not dynamic