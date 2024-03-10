import time
from keyboard_server.serial_backend import *
from keyboard_server.keycodes import *
from keyboard_server.utils import *

from utils.constants import *

NULL_CHAR = chr(0)

# This test clearly proves that there is nothing wrong with the dongle
# or the key events when they are sent in bursts..

class KeyPresser:
    def __init__(self, backend):
        self.backend = backend
        self.active_modifiers = set()

    def press_key(self, key):
        if key in [0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7]:
            self.press_modifier(key)
            return
        # Construct the first char of the report using the active modifiers
        first_char = NULL_CHAR
        # Set each bit corresponding to a modifier key that is currently active
        # The bit index can be taken from 0xeX where X is the bit index
        for modifier in self.active_modifiers:
            first_char = chr(ord(first_char) | (1 << (modifier - 0xe0)))
        self.write_report(first_char+NULL_CHAR+chr(key)+NULL_CHAR*5)

    def press_modifier(self, modifier):
        self.active_modifiers.add(modifier)

    def release_modifier(self, modifier):
        if modifier in self.active_modifiers:
            self.active_modifiers.remove(modifier)

    def release_key(self, key):
        if key in [0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7]:
            self.release_modifier(key)
            return
        self.write_report(NULL_CHAR*8)

    def write_report(self, report):
        self.backend.write(report)

def main():
    # Your code here
    backend = Serial_Backend()
    key_presser = KeyPresser(backend)

    # write ten consecutive key presses
    for i in range(10):
        hid_key = key_name_to_hid_report_code[qwerty_to_colemak_dh("KEY_R")]
        key_presser.press_key(hid_key)
        key_presser.release_key(hid_key)

    hid_key = key_name_to_hid_report_code[qwerty_to_colemak_dh("KEY_COMMA")]
    key_presser.press_key(hid_key)
    key_presser.release_key(hid_key)

    for i in range(10):

        for i in range(250):
            hid_key = key_name_to_hid_report_code[qwerty_to_colemak_dh("KEY_Q")]
            key_presser.press_key(hid_key)
            key_presser.release_key(hid_key)
        
        for i in range(250):
            hid_key = key_name_to_hid_report_code[qwerty_to_colemak_dh("KEY_BACKSPACE")]
            key_presser.press_key(hid_key)
            key_presser.release_key(hid_key)

        time.sleep(1.8 * 2.5)

if __name__ == "__main__":
    main()