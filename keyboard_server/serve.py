import argparse
import socket
import threading
import subprocess
import os

from keyboard_server.keycodes import *
from keyboard_server.serial_backend import *
from keyboard_server.virtual_backend import *
from keyboard_server.utils import *
from keyboard_server.doublethink import *
from utils.constants import *

NULL_CHAR = chr(0)

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

class KeyboardServer:
    def __init__(self, backend='virtual', incoming_command_ckb = None):
        self.virtual_backend = False
        if backend == 'virtual':
            self.backend = Virtual_Backend()
            self.virtual_backend = True
        else:
            self.backend = Serial_Backend()

        self.key_presser = KeyPresser(self.backend)
        self.ip = subprocess.check_output(["tailscale", "ip", "-4"]).decode("utf-8").strip()
        self.incoming_command_ckb = incoming_command_ckb
        self.win_lang = "SV"

        # Tribute to 1984
        # The Doubluthinks shall be selectable by the user if active or not
        self.dts = {'se': Doublethink('se'), 'en_talon': Doublethink('en'), 'en_win': Doublethink('en')}

        self.dts['se'].set_emit_keyevent(self.handle_keyevent)
        self.dts['en_talon'].set_emit_keyevent(self.handle_keyevent)
        self.dts['en_win'].set_emit_keyevent(self.handle_keyevent)

        self.dt = None

    def key_press(self, key):
        pressed_key = x11_key_code_to_name[key]
        if pressed_key == 'SPEC_KEY_Ä':
            self.key_press(get_x11_keycode_from_name("KEY_RIGHTALT"));
            self.key_press(get_x11_keycode_from_name("KEY_R"));

            self.key_release(get_x11_keycode_from_name("KEY_R"));
            self.key_release(get_x11_keycode_from_name("KEY_RIGHTALT"));
            return
        elif pressed_key == 'SPEC_KEY_Ö':
            self.key_press(get_x11_keycode_from_name("KEY_RIGHTALT"));
            self.key_press(get_x11_keycode_from_name("KEY_O"));

            self.key_release(get_x11_keycode_from_name("KEY_O"));
            self.key_release(get_x11_keycode_from_name("KEY_RIGHTALT"));
            return
        elif pressed_key == 'SPEC_KEY_Å':
            self.key_press(get_x11_keycode_from_name("KEY_RIGHTALT"));
            self.key_press(get_x11_keycode_from_name("KEY_A"));

            self.key_release(get_x11_keycode_from_name("KEY_A"));
            self.key_release(get_x11_keycode_from_name("KEY_RIGHTALT"));
            return
        colemak_key = qwerty_to_colemak_dh(pressed_key)
        if self.virtual_backend:
            self.backend.key_press(colemak_key)
            return
        hid_key = key_name_to_hid_report_code[colemak_key]
        self.key_presser.press_key(hid_key)

        return 'Key press received: {}'.format(key)

    def key_release(self, key):
        pressed_key = x11_key_code_to_name[key]
        if pressed_key.startswith('SPEC_KEY_'):
            # These are handled as macros on key press
            return
        colemak_key = qwerty_to_colemak_dh(pressed_key)
        if self.virtual_backend:
            self.backend.key_release(colemak_key)
            return
        hid_key = key_name_to_hid_report_code[colemak_key]
        self.key_presser.release_key(hid_key)

        return 'Key release received: {}'.format(key)

    def handle_keyevent(self, keycode, event_type):
        """Handle a key event."""
        if event_type == 0:
            self.key_press(keycode)
        elif event_type == 1:
            self.key_release(keycode)
        else:
            print(f"Unknown event type: {event_type}")

    def prepare_win_state(self):
        self.state = self.state.win_run
        self.key_buffer = []

    def handle_incoming_command(self, cmd):
        if cmd != "toggle_win_lang" and self.incoming_command_ckb:
            self.incoming_command_ckb(cmd)
        if cmd == "stop":
            self.dt = None
            send_udp_string("engine_win11_swe", 5000, "stop")
            send_udp_string("engine_talon", 5000, "stop")
            send_udp_string("engine_talon", 5005, "stop")
        elif cmd == "start_talon_command":
            self.dt = None
            send_udp_string("engine_win11_swe", 5000, "stop")
            send_udp_string("engine_talon", 5005, "stop")
            send_udp_string("engine_talon", 5000, "start_command@{}".format(self.ip))
        elif cmd == "start_talon_dictation":
            self.dt = self.dts['en_talon']
            self.dt.arm()
            send_udp_string("engine_win11_swe", 5000, "stop")
            send_udp_string("engine_talon", 5005, "stop")
            send_udp_string("engine_talon", 5000, "start_dictation@{}".format(self.ip))
        elif cmd == "start_win11_swe":
            if self.win_lang == "SV":
                self.dt = self.dts['se']
            elif self.win_lang == "EN":
                self.dt = self.dts['en_win']
            self.dt.arm()
            send_udp_string("engine_talon", 5000, "stop")
            send_udp_string("engine_talon", 5005, "stop")
            send_udp_string("engine_win11_swe", 5000, "start@{}".format(self.ip))
        elif cmd == "start_gdocs":
            send_udp_string("engine_win11_swe", 5000, "stop")
            send_udp_string("engine_talon", 5000, "stop")
            send_udp_string("engine_talon", 5005, "start@{}".format(self.ip))
        elif cmd == "toggle_win_lang":
            send_udp_string("engine_win11_swe", 5000, "toggle-lang")
            # Since we dont want to freeze the thread we call the callback here
            if self.incoming_command_ckb:
                self.incoming_command_ckb(cmd)

    def handle_incoming_command_key(self, key):
        if key == 'f1':
            self.handle_incoming_command("start_talon_command")
        elif key == 'f2':
            self.handle_incoming_command("start_win11_swe")
        elif key == 'f3':
            if self.dt == None:
                self.handle_incoming_command("start_talon_dictation")
            else:
                self.dt.redo()
        elif key == 'f4':
            if self.dt != None:
                self.dt.undo()
        elif key == 'f8':
            pass
        elif key == 'f9':
            pass
        elif key == 'f10':
            pass
        elif key == 'f11':
            pass
        elif key == 'f12':
            self.handle_incoming_command("stop")

    def command_server(self):
        # create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # bind socket to address and port
        sock.bind(("0.0.0.0", int(LOCAL_SERVER_PORT)))

        while True:
            data, addr = sock.recvfrom(1024)
            key = data.decode()
            self.handle_incoming_command_key(key)
            continue
            self.handle_incoming_command(cmd)

    def run(self):
        self.command_server_thread = threading.Thread(target=self.command_server)
        self.command_server_thread.start()

        # create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # bind socket to address and port
        sock.bind(("0.0.0.0", int(VOICE_BOX_CLIENT_PORT)))

        # event loop
        while True:
            data, addr = sock.recvfrom(1024)
            try:
                message = data.decode()
            except Exception as e:
                print(f"Invalid message: {data}")
                continue
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
            if self.dt:
                self.dt.handle_keyevent(keycode, event_type)
            else:
                self.handle_keyevent(keycode, event_type)

        # cleanup
        sock.close()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # Create KeyboardServer instance and run it
    server = KeyboardServer()
    server.run()


if __name__ == '__main__':
    main()
