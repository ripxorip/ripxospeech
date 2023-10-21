import argparse
import flask
import sys

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

x11_key_code_to_name = {
    0x09: "KEY_ESC",
    0x0A: "KEY_1",
    0x0B: "KEY_2",
    0x0C: "KEY_3",
    0x0D: "KEY_4",
    0x0E: "KEY_5",
    0x0F: "KEY_6",
    0x10: "KEY_7",
    0x11: "KEY_8",
    0x12: "KEY_9",
    0x13: "KEY_0",
    0x14: "KEY_MINUS",
    0x15: "KEY_EQUAL",
    0x16: "KEY_BACKSPACE",
    0x17: "KEY_TAB",
    0x18: "KEY_Q",
    0x19: "KEY_W",
    0x1A: "KEY_E",
    0x1B: "KEY_R",
    0x1C: "KEY_T",
    0x1D: "KEY_Y",
    0x1E: "KEY_U",
    0x1F: "KEY_I",
    0x20: "KEY_O",
    0x21: "KEY_P",
    0x22: "KEY_LEFTBRACE",
    0x23: "KEY_RIGHTBRACE",
    0x24: "KEY_ENTER",
    0x25: "KEY_LEFTCTRL",
    0x26: "KEY_A",
    0x27: "KEY_S",
    0x28: "KEY_D",
    0x29: "KEY_F",
    0x2A: "KEY_G",
    0x2B: "KEY_H",
    0x2C: "KEY_J",
    0x2D: "KEY_K",
    0x2E: "KEY_L",
    0x2F: "KEY_SEMICOLON",
    0x30: "KEY_APOSTROPHE",
    0x31: "KEY_GRAVE",
    0x32: "KEY_LEFTSHIFT",
    0x33: "KEY_BACKSLASH",
    0x34: "KEY_Z",
    0x35: "KEY_X",
    0x36: "KEY_C",
    0x37: "KEY_V",
    0x38: "KEY_B",
    0x39: "KEY_N",
    0x3A: "KEY_M",
    0x3B: "KEY_COMMA",
    0x3C: "KEY_DOT",
    0x3D: "KEY_SLASH",
    0x3E: "KEY_RIGHTSHIFT",
    0x3F: "KEY_KPASTERISK",
    0x40: "KEY_LEFTALT",
    0x41: "KEY_SPACE",
    0x42: "KEY_CAPSLOCK",
    0x43: "KEY_F1",
    0x44: "KEY_F2",
    0x45: "KEY_F3",
    0x46: "KEY_F4",
    0x47: "KEY_F5",
    0x48: "KEY_F6",
    0x49: "KEY_F7",
    0x4A: "KEY_F8",
    0x4B: "KEY_F9",
    0x4C: "KEY_F10",
    0x4D: "KEY_NUMLOCK",
    0x4E: "KEY_SCROLLLOCK",
    0x4F: "KEY_KP7",
    0x50: "KEY_KP8",
    0x51: "KEY_KP9",
    0x52: "KEY_KPMINUS",
    0x53: "KEY_KP4",
    0x54: "KEY_KP5",
    0x55: "KEY_KP6",
    0x56: "KEY_KPPLUS",
    0x57: "KEY_KP1",
    0x58: "KEY_KP2",
    0x59: "KEY_KP3",
    0x5A: "KEY_KP0",
    0x5B: "KEY_KPDOT",
    0x5D: "KEY_ZENKAKUHANKAKU",
    0x5E: "KEY_102ND",
    0x5F: "KEY_F11",
    0x60: "KEY_F12",
    0x61: "KEY_RO",
    0x62: "KEY_KATAKANA",
    0x63: "KEY_HIRAGANA",
    0x64: "KEY_HENKAN",
    0x65: "KEY_KATAKANAHIRAGANA",
    0x66: "KEY_MUHENKAN",
    0x67: "KEY_KPJPCOMMA",
    0x68: "KEY_KPENTER",
    0x69: "KEY_RIGHTCTRL",
    0x6A: "KEY_KPSLASH",
    0x6B: "KEY_SYSRQ",
    0x6C: "KEY_RIGHTALT",
    0x6D: "KEY_LINEFEED",
    0x6E: "KEY_HOME",
    0x6F: "KEY_UP",
    0x70: "KEY_PAGEUP",
    0x71: "KEY_LEFT",
    0x72: "KEY_RIGHT",
    0x73: "KEY_END",
    0x74: "KEY_DOWN",
    0x75: "KEY_PAGEDOWN",
    0x76: "KEY_INSERT",
    0x77: "KEY_DELETE",
    0x78: "KEY_MACRO",
    0x79: "KEY_MUTE",
    0x7A: "KEY_VOLUMEDOWN",
    0x7B: "KEY_VOLUMEUP",
    0x7C: "KEY_POWER",
    0x7D: "KEY_KPEQUAL",
    0x7E: "KEY_KPPLUSMINUS",
    0x7F: "KEY_PAUSE",
    0x80: "KEY_SCALE",
    0x81: "KEY_KPCOMMA",
    0x82: "KEY_HANGUEL",
    0x83: "KEY_HANJA",
    0x84: "KEY_YEN",
    0x85: "KEY_LEFTMETA",
    0x86: "KEY_RIGHTMETA",
    0x87: "KEY_COMPOSE"
}

# TODO Create a corresponding dictionary for key names to key HID report codes

class KeyboardServer:
    def __init__(self):
        # Create Flask app
        self.app = flask.Flask(__name__)

        # Add routes for key press and key release
        self.app.add_url_rule('/key_press', 'key_press', self.key_press, methods=['POST'])
        self.app.add_url_rule('/key_release', 'key_release', self.key_release, methods=['POST'])

    def key_press(self):
        key = flask.request.form['key']
        # Parse the key code from hex string to integer
        key = int(key, 16)
        # Print key as hex
        print('Pressed key: {}'.format(x11_key_code_to_name[key]))
        # Do something with the key press
        return 'Key press received: {}'.format(key)

    def key_release(self):
        key = flask.request.form['key']
        # Do something with the key release
        return 'Key release received: {}'.format(key)

    def run(self):
        # Run Flask app on all interfaces
        self.app.run(host='0.0.0.0')


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # Create KeyboardServer instance and run it
    server = KeyboardServer()
    server.run()


if __name__ == '__main__':
    main()
