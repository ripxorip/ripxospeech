import os
import time
from keyboard_server.keycodes import *
from utils.dongle_utils import *
from utils.constants import *
import socket

class Virtual_Backend:
    def __init__(self):
        pass

    def key_press(self, key):
        print("key_press: " + key)
        self.write(chr(keyname_to_linux_event_code[key]) + chr(0))

    def key_release(self, key):
        print("key_release: " + key)
        self.write(chr(keyname_to_linux_event_code[key]) + chr(1))

    def write(self, report):
        # Send the report to the local server 127.0.0.1 on port 8734
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(report.encode(), ("127.0.0.1", 8734))
        sock.close()