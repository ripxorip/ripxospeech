import os
import time
from keyboard_server.keycodes import *
from utils.dongle_utils import *
from utils.constants import *
import socket

class Virtual_Backend:
    def __init__(self, read_cb):
        self.read_cb = read_cb

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

    def read_thread(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", int(LOCAL_SERVER_PORT)))

        while True:
            data, addr = sock.recvfrom(1024)
            # read data from HID device
            # Print the data as hex with a space between each byte
            print('Got data: ', end='')
            print(' '.join(format(x, '02x') for x in data))
            command = data[0]
            self.read_cb(command)