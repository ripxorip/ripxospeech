import threading
import subprocess
import os
import signal
import socket
import time

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

        self.running_engine = "stop"

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

        self.dongle_path = get_dongle_serial_port()
        self.update_gui_state()

    def get_win_lang(self):
        req_str = "get-current-lang"
        # Send the string to 127.0.0.1 5000 and receive the response
        bytes = req_str.encode('utf-8')
        # Send the specified bytes to the specified server over UDP using socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes, (IP_ADDR["engine_win11_swe"], 5000))
        # Receive the response
        sock.settimeout(1)
        data,_ = sock.recvfrom(1024)
        lang = data.decode('utf-8')
        print(lang)
        if lang == "sv-SE":
            lang = "SV"
        elif lang == "en-US":
            lang = "EN"
        return lang

    def toggle_win_lang(self):
        req_str = "toggle-lang"
        bytes = req_str.encode('utf-8')
        # Send the string to
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes, (IP_ADDR["engine_win11_swe"], 5000))
        time.sleep(0.5)
        self.update_gui_state()
        print(self.winLang)
        self.gui_callback(self.gui_state)

    def keyboard_server(self):
        backend = 'hid'
        if usb_dongle_is_connected():
            backend = 'serial'
        print("Starting keyboard server with backend: {}".format(backend))
        from keyboard_server.serve import KeyboardServer
        self.server = KeyboardServer(backend=backend, incoming_command_ckb=self.dictation_command_cbk)
        self.server.run()

    def clicked_button_incoming_command(self, command):
        self.server.handle_incoming_command(KEYBOARD_SERVER_COMMANDS[command])

    def set_gui_callback(self, callback):
        self.gui_callback = callback

    def update_gui_state(self):
        self.winLang = self.get_win_lang()
        statusText = "Active"
        self.gui_state['buttons']['talonCommand']['active'] = False
        self.gui_state['buttons']['talonSentence']['active'] = False
        self.gui_state['buttons']['winRun']['active'] = False

        if self.running_engine == "stop":
            statusText = "Idle"
        elif self.running_engine == "start_talon_command":
            self.gui_state['buttons']['talonCommand']['active'] = True
        elif self.running_engine == "start_talon_dictation":
            self.gui_state['buttons']['talonSentence']['active'] = True
        elif self.running_engine == "start_win11_swe":
            self.gui_state['buttons']['winRun']['active'] = True
        elif self.running_engine == "start_gdocs":
            pass
        self.gui_state['labels']['statusText'] = "Status: " + statusText + ", Dongle: " + self.dongle_path
        self.gui_state['labels']['winLang'] = "Lang: " + self.winLang

    # Called when a dictation command is trigged using a manual key press like F8-F12 on Gnome
    def dictation_command_cbk(self, command):
        cmd = ""
        for key, value in KEYBOARD_SERVER_COMMANDS.items():
            if value == command:
                cmd = key
        if cmd != "":
            self.running_engine = cmd
            if cmd == "stop":
                self.stop_audio_stream()
            else:
                self.start_audio_stream()
            self.update_gui_state()
            self.gui_callback(self.gui_state)

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

        if button == 'talonCommand':
            self.clicked_button_incoming_command("start_talon_command")
        elif button == 'talonSentence':
            self.clicked_button_incoming_command("start_talon_dictation")
        elif button == 'winRun':
            self.clicked_button_incoming_command("start_win11_swe") 
        elif button == 'stop':
            self.clicked_button_incoming_command("stop")
        elif button == 'winSV':
            if self.winLang == "EN":
                self.toggle_win_lang()
        elif button == 'winEN':
            if self.winLang == "SV":
                self.toggle_win_lang()