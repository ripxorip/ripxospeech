import socket
from utils.constants import *
from keyboard_server.keycodes import *

def get_x11_keycode_from_name(name):
    ret = None
    for key, value in x11_key_code_to_name.items():
        if value == name:
            ret = key
            break
    return ret

def send_udp_string(server, port, string):
    # Convert the string to bytes
    bytes = string.encode('utf-8')
    # Send the specified bytes to the specified server over UDP using socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes, (IP_ADDR[server], port))
