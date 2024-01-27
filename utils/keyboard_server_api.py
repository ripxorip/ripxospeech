import os
import subprocess
import socket
from utils.constants import *

def get_hid_raw_filename(usb_id):
    ret = subprocess.check_output(["ls", "/sys/class/hidraw"]).decode("utf-8").strip().splitlines()
    # Find which hidraw device is the USB device
    for r in ret:
        # Get the USB ID of the device
        p = os.path.join("/sys/class/hidraw", r, "device")
        if os.path.islink(p):
            # Get the target of the link
            target = os.readlink(p)
            # Check if the target contains the USB ID
            if usb_id in target:
                return r
    print('Info: Could not find the USB device with USB ID: {}'.format(usb_id))
    return None

def send_string_to_ripxovoice_hid(s):
    os.system("echo -ne '{}' | sudo tee /dev/{}".format(s, get_hid_raw_filename("1D6B:0104")))

def usb_dongle_is_connected():
    return get_hid_raw_filename("CAFE:4005") != None

def send_command_to_keyboard_server(command):
    addr = "127.0.0.1"
    port = int(LOCAL_SERVER_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(command.encode(), (addr, port))
    sock.close()