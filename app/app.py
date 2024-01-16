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

    def keyboard_server(self):
        backend = 'hid'
        if usb_dongle_is_connected():
            backend = 'serial'
        print("Starting keyboard server with backend: {}".format(backend))
        from keyboard_server.serve import KeyboardServer
        server = KeyboardServer(backend=backend, incoming_command_ckb=self.dictation_command_cbk)
        server.run()

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

    def button_clicked(self, button):
        print("button clicked")

    def start_keyboard_server(self):
        print("start_keyboard_server")

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