import argparse
import socket
import threading
import subprocess
import os

from keyboard_server.keycodes import *
from utils.constants import *

NULL_CHAR = chr(0)

class KeyPresser:
    def __init__(self):
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
        with open('/dev/hidg0', 'rb+') as fd:
            fd.write(report.encode())


class KeyboardServer:
    def __init__(self):
        self.key_presser = KeyPresser()
        self.ip = subprocess.check_output(["tailscale", "ip", "-4"]).decode("utf-8").strip()

    def key_press(self, key):
        pressed_key = x11_key_code_to_name[key]
        colemak_key = qwerty_to_colemak_dh(pressed_key)
        hid_key = key_name_to_hid_report_code[colemak_key]
        print('Press Key: {}, Colemak key: {}, HID key: {}'.format(pressed_key, colemak_key, hid_key))
        self.key_presser.press_key(hid_key)

        return 'Key press received: {}'.format(key)

    def key_release(self, key):
        pressed_key = x11_key_code_to_name[key]
        colemak_key = qwerty_to_colemak_dh(pressed_key)
        hid_key = key_name_to_hid_report_code[colemak_key]
        print('Release key: {}, Colemak key: {}, HID key: {}'.format(pressed_key, colemak_key, hid_key))
        self.key_presser.release_key(hid_key)

        return 'Key release received: {}'.format(key)

    def handle_keyevent(self, keycode, event_type):
        """Handle a key event."""
        if event_type == 0:
            self.key_press(keycode)
            # handle key press event
        elif event_type == 1:
            self.key_release(keycode)
            # handle key release event
        else:
            print(f"Unknown event type: {event_type}")

    def send_udp_string(self, server, port, string):
        # Convert the string to bytes
        bytes = string.encode('utf-8')
        # Send the specified bytes to the specified server over UDP using socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes, (IP_ADDR[server], port))

    def handle_command(self, command):
        cmd = ""
        for key, value in HID_COMMANDS.items():
            if value == command:
                cmd = key
        if cmd == "stop":
            self.send_udp_string("engine_win11_swe", 5000, "stop")
            self.send_udp_string("engine_talon", 5000, "stop")
            self.send_udp_string("engine_talon", 5005, "stop")
        elif cmd == "start_talon_command":
            self.send_udp_string("engine_talon", 5000, "start_command@{}".format(self.ip))
        elif cmd == "start_talon_dictation":
            self.send_udp_string("engine_talon", 5000, "start_dictation@{}".format(self.ip))
        elif cmd == "start_win11_swe":
            self.send_udp_string("engine_win11_swe", 5000, "start@{}".format(self.ip))
        elif cmd == "start_gdocs":
            self.send_udp_string("engine_talon", 5005, "start@{}".format(self.ip))

    def read_hid(self):
        """Read data from HID device."""
        while True:
            # read data from HID device
            hid_data = os.read(self.hid_fd, 1024)
            # Print the data as hex with a space between each byte
            print('Got data: ', end='')
            print(' '.join(format(x, '02x') for x in hid_data))
            command = hid_data[0]
            self.handle_command(command)

    def run(self):
        """Event loop for UDP."""
        # create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.hid_fd = os.open('/dev/hidg0', os.O_RDONLY)

        # create and start thread for HID device
        self.hid_thread = threading.Thread(target=self.read_hid)
        self.hid_thread.start()

        # bind socket to address and port
        sock.bind(("0.0.0.0", int(VOICE_BOX_CLIENT_PORT)))

        # event loop
        while True:
            data, addr = sock.recvfrom(1024)
            message = data.decode()
            parts = message.split(",")
            if len(parts) != 2:
                print(f"Invalid message: {message}")
                continue
            try:
                keycode = int(parts[0], 16)
                event_type = int(parts[1])
            except ValueError:
                print(f"Invalid message: {message}")
                continue
            self.handle_keyevent(keycode, event_type)

        # cleanup
        sock.close()
        os.close(hid_fd)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # Create KeyboardServer instance and run it
    server = KeyboardServer()
    server.run()


if __name__ == '__main__':
    main()
