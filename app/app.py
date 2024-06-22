import threading
import subprocess
import os
import signal
import socket
import time

from PIL import Image
from io import BytesIO
import pytesseract

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
        if self.dongle_path is None:
            self.dongle_path = "Virtual"
        self.get_win_lang()
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

        # Convert the data to an image
        image = Image.open(BytesIO(data))

        # Use pytesseract to extract text from the image
        lang = pytesseract.image_to_string(image)
        print('Detected language: ', lang)
        lang = lang.strip()

        write_image = False
        # Writh the data as a jpg file
        if write_image:
            with open('lang.jpg', 'wb') as f:
                f.write(data)
        if lang == "Swe":
            lang = "SV"
        elif lang == "ENG":
            lang = "EN"
        self.winLang = lang
        # FIXME This is too hacky
        self.server.win_lang = lang
        return lang

    def keyboard_server(self):
        backend = 'virtual'
        if usb_dongle_is_connected():
            backend = 'serial'
        print("Starting keyboard server with backend: {}".format(backend))
        if backend == 'virtual':
            print('Starting virtual keyboard server')
            self.virtual_keyboard_server = subprocess.Popen(["sudo", "virtual_keyboard"], preexec_fn=os.setsid)
        from keyboard_server.serve import KeyboardServer
        self.server = KeyboardServer(backend=backend, incoming_command_ckb=self.dictation_command_cbk)
        self.server.run()

    def set_gui_callback(self, callback):
        self.gui_callback = callback

    def update_gui_state(self):
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
    def dictation_command_cbk(self, cmd):
        if cmd == "toggle_win_lang":
            time.sleep(4)
            self.get_win_lang()
            self.update_gui_state()
            self.gui_callback(self.gui_state)
        elif cmd == "get_win_lang":
            return self.get_win_lang()
        elif cmd != "":
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

        # UPDATE: Now that I have developed ripxostream, it will be started manually for now..
        #if self.stream_process is None:
        #    self.stream_process = subprocess.Popen(["linux_gstreamer_client/stream.sh"], preexec_fn=os.setsid)
        self.send_command_to_sound_host("start")

    def stop_audio_stream(self):
        # Shall stop the local gstreamer pipeline
        # and send a message to the gstreamer server to stop listening

        # UPDATE: Now that I have developed ripxostream, it will be started manually for now..
        #if self.stream_process is not None:
        #    os.killpg(os.getpgid(self.stream_process.pid), signal.SIGINT)
        #    self.stream_process = None
        self.send_command_to_sound_host("stop")

    def teardown(self):
        self.stop_audio_stream()
        self.send_command_to_sound_host("stop")
        # send 0xdeadbef0 to kill each thread
        # Print out information about all currently running threads
        bytes = "0xdeadbeef".encode('utf-8')
        # Send the specified bytes to the specified server over UDP using socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes, ("127.0.0.1", int(LOCAL_SERVER_PORT)))
        sock.sendto(bytes, ("127.0.0.1", int(VOICE_BOX_CLIENT_PORT)))

        # Kill the virtual keyboard server
        bytes = 0xdeadbeef.to_bytes(4)
        sock.sendto(bytes, ("127.0.0.1", int(8734)))

    def gui_button_clicked(self, button):
        # Just to get the initial state correct
        if button is None:
            self.gui_callback(self.gui_state)
            return

        if button == 'talonCommand':
            self.server.handle_incoming_command("start_talon_command")
        elif button == 'talonSentence':
            self.server.handle_incoming_command("start_talon_dictation")
        elif button == 'winRun':
            self.server.handle_incoming_command("start_win11_swe") 
        elif button == 'stop':
            self.server.handle_incoming_command("stop")
        elif button == 'talonConfig':
            # Open the browser to http://voiceboxlinux:8443/?folder=/talon
            os.system("xdg-open http://voiceboxlinux:8443/?folder=/talon")
        elif button == 'winSV':
            if self.winLang == "EN":
                self.server.handle_incoming_command("toggle_win_lang")
        elif button == 'winEN':
            if self.winLang == "SV":
                self.server.handle_incoming_command("toggle_win_lang")
