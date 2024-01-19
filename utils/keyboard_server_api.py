import os
import subprocess
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

def send_string_to_local_server(s):
    addr = "127.0.0.1"
    port = LOCAL_SERVER_PORT
    print(s)
    os.system("echo -ne '{}' | nc -u {} {}".format(s, addr, port))

def usb_dongle_is_connected():
    return get_hid_raw_filename("CAFE:4005") != None

def send_command_to_keyboard_server(command):
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
    send_string_to_local_server(s)