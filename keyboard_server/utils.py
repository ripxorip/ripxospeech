import socket
from utils.constants import *

def send_udp_string(server, port, string):
    # Convert the string to bytes
    bytes = string.encode('utf-8')
    # Send the specified bytes to the specified server over UDP using socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes, (IP_ADDR[server], port))

def util_handle_command(command, ip):
    cmd = ""
    for key, value in KEYBOARD_SERVER_COMMANDS.items():
        if value == command:
            cmd = key
    if cmd == "stop":
        send_udp_string("engine_win11_swe", 5000, "stop")
        send_udp_string("engine_talon", 5000, "stop")
        send_udp_string("engine_talon", 5005, "stop")
    elif cmd == "start_talon_command":
        send_udp_string("engine_win11_swe", 5000, "stop")
        send_udp_string("engine_talon", 5005, "stop")
        send_udp_string("engine_talon", 5000, "start_command@{}".format(ip))
    elif cmd == "start_talon_dictation":
        send_udp_string("engine_win11_swe", 5000, "stop")
        send_udp_string("engine_talon", 5005, "stop")
        send_udp_string("engine_talon", 5000, "start_dictation@{}".format(ip))
    elif cmd == "start_win11_swe":
        send_udp_string("engine_talon", 5000, "stop")
        send_udp_string("engine_talon", 5005, "stop")
        send_udp_string("engine_win11_swe", 5000, "start@{}".format(ip))
    elif cmd == "start_gdocs":
        send_udp_string("engine_win11_swe", 5000, "stop")
        send_udp_string("engine_talon", 5000, "stop")
        send_udp_string("engine_talon", 5005, "start@{}".format(ip))