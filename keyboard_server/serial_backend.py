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
    def __init__(self):
        self.serial_port = serial.Serial(get_dongle_serial_port())

    def write(self, report):
        # Print the datatype of report
        data = report.encode()
        hex_str = ''
        for i in data:
            hex_str += '\\x{:02x}'.format(i)
        self.serial_port.write(data)