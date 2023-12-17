# This backend is used together with an embedded device such as the rp2040.
# Each report is sent to the device over serial and the device sends the corresponding HID report
# to the host as a keyboard. The communication from the backend comes from UDP/IP instead of hid packets

import os
import time
from utils.dongle_utils import *
from utils.constants import *
import socket
import serial

class Serial_Backend:
    def __init__(self, read_cb):
        self.serial_port = serial.Serial(get_dongle_serial_port())
        self.read_cb = read_cb

    def write(self, report):
        # Print the datatype of report
        data = report.encode()
        hex_str = ''
        for i in data:
            hex_str += '\\x{:02x}'.format(i)
        self.serial_port.write(data)

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