#!/usr/bin/env python

import subprocess
import argparse
import os

from utils.constants import *
from utils.tmux import *
from utils.keyboard_server_api import *


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Tool to use for routing my voice to different speech recognition servers")
    # Add the arguments
    parser.add_argument("-a", "--action", help="The action to perform", choices=["serve", "kill", "route", "start_dictation", "stop_dictation"], required=True)
    parser.add_argument("-c", "--client", help="The client to use", choices=["work", "station"])
    parser.add_argument("-e", "--engine", help="the speech engine to use", choices=["talon_dictation", "talon_command", "win11_swe", "gdocs"])
    # Parse the arguments
    args = parser.parse_args()

    if args.action == "route":
        tmux_run(
            "gst-launch-1.0 -v pulsesrc buffer-time=100000 latency-time=10000 ! opusenc ! "
            "rtpopuspay ! queue max-size-buffers=200 max-size-time=20000000 max-size-bytes=2000 ! "
            "multiudpsink clients={}:{},{}:{} buffer-size=200".format(
                IP_ADDR["engine_talon"], GST_SOUND_PORT, IP_ADDR["engine_win11_swe"], GST_SOUND_PORT
            ), 
            args.client
        )

    elif args.action == "kill":
        tmux_kill()

    elif args.action == "serve":
        from keyboard_server.serve import KeyboardServer
        server = KeyboardServer()
        server.run()

    elif args.action == "start_dictation":

        if args.engine == "talon_dictation":
            send_command_to_keyboard_server("start_talon_dictation")

        elif args.engine == "talon_command":
            send_command_to_keyboard_server("start_talon_command")

        elif args.engine == "win11_swe":
            send_command_to_keyboard_server("start_win11_swe")

        elif args.engine == "gdocs":
            send_command_to_keyboard_server("start_gdocs")

    elif args.action == "stop_dictation":
        send_command_to_keyboard_server("stop")

if __name__ == "__main__":
    main()
