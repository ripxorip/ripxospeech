import threading
import subprocess
import os
import signal
import socket

from utils.dongle_utils import *
from utils.keyboard_server_api import *
from utils.constants import *

class App:
    def __init__(self):
        self.stream_process = None
        self.sound_host_ip = "100.101.164.159"
        self.sound_host_port = 1538
        self.send_command_to_sound_host("stop")
        self.keyboard_server_thread = threading.Thread(target=self.keyboard_server)
        self.keyboard_server_thread.start()

        self.gui_state = {
            'buttons': {
                'talonCommand': {
                    'label': 'Talon Command',
                    'text': 'Talon Command',
                    'active': False,
                },
                'talonSentence': {
                    'label': 'Talon Sentence',
                    'text': 'Talon Sentence',
                    'active': False,
                },
                'winRun': {
                    'label': 'Win Run',
                    'text': 'Win',
                    'active': False,
                },
                'winSV': {
                    'label': 'Win SV',
                    'active': False,
                },
                'winEN': {
                    'label': 'Win EN',
                    'active': False,
                },
            },
            'labels': {
                'winLang': 'Lang: SV',
                'statusText': 'Status: Idle, Dongle: USB',
            },
            'toggles': {
            },
        }

    def keyboard_server(self):
        backend = 'hid'
        if usb_dongle_is_connected():
            backend = 'serial'
        print("Starting keyboard server with backend: {}".format(backend))
        from keyboard_server.serve import KeyboardServer
        self.server = KeyboardServer(backend=backend, incoming_command_ckb=self.dictation_command_cbk)
        self.server.run()

    def clicked_button_incoming_command(self, command):
        b = [KEYBOARD_SERVER_COMMANDS[command]]
        # Send the bytes to the device like
        # echo -ne '\x01\x00\x00\x00' | sudo dd of=/dev/hidraw5 bs=4 conv=notrunc
        # Convert the bytes to a string like \x01\x00\x00\x00
        # Make sure that the size of the bytes is a multiple of 4
        # Otherwise pad with 0s
        while len(b) % 4 != 0:
            b.append(0)
        s = ""
        for i in b:
            s += "\\x{:02x}".format(i)
        self.server.handle_incoming_command(s)

    def set_gui_callback(self, callback):
        self.gui_callback = callback

    # Called when a dictation command is trigged using a manual key press like F8-F12 on Gnome
    def dictation_command_cbk(self, command):
        cmd = ""
        for key, value in KEYBOARD_SERVER_COMMANDS.items():
            if value == command:
                cmd = key
        if cmd != "":
            if cmd == "stop":
                self.stop_audio_stream()
            else:
                self.start_audio_stream()

    def send_command_to_sound_host(self, command):
        bytes = command.encode('utf-8')
        # Send the specified bytes to the specified server over UDP using socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes, (self.sound_host_ip, self.sound_host_port))

    def start_audio_stream(self):
        # Shall start the local gstreamer pipeline
        # and send a message to the gstreamer server to start listening
        # Set os.setsid() to make it run in a new process group,
        # that way we can kill the entire process group when we want to stop the stream
        if self.stream_process is None:
            self.stream_process = subprocess.Popen(["linux_gstreamer_client/stream.sh"], preexec_fn=os.setsid)
        self.send_command_to_sound_host("start")

    def stop_audio_stream(self):
        # Shall stop the local gstreamer pipeline
        # and send a message to the gstreamer server to stop listening
        if self.stream_process is not None:
            os.killpg(os.getpgid(self.stream_process.pid), signal.SIGINT)
            self.stream_process = None
        self.send_command_to_sound_host("stop")

    def teardown(self):
        self.stop_audio_stream()
        self.send_command_to_sound_host("stop")

    def gui_button_clicked(self, button):
        # Just to get the initial state correct
        if button is None:
            self.gui_callback(self.gui_state)
            return

        self.gui_state['buttons'][button]['active'] = not self.gui_state['buttons'][button]['active']
        self.gui_callback(self.gui_state)