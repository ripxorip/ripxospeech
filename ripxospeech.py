#!/usr/bin/env python

import subprocess
import argparse
import os

from utils.constants import *
from utils.tmux import *
from utils.keyboard_server_api import *

def route(args):
    tmux_run(
        "./linux_gstreamer_client/stream.sh",
        args.client
    )

def kill():
    tmux_kill()

def serve():
    from keyboard_server.serve import KeyboardServer
    server = KeyboardServer()
    server.run()

def start_dictation(args):
    if args.engine == "talon_dictation":
        send_command_to_keyboard_server("start_talon_dictation")
    elif args.engine == "talon_command":
        send_command_to_keyboard_server("start_talon_command")
    elif args.engine == "win11_swe":
        send_command_to_keyboard_server("start_win11_swe")
    elif args.engine == "gdocs":
        send_command_to_keyboard_server("start_gdocs")

def stop_dictation():
    send_command_to_keyboard_server("stop")

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
        route(args)
    elif args.action == "kill":
        kill()
    elif args.action == "serve":
        serve()
    elif args.action == "start_dictation":
        start_dictation(args)
    elif args.action == "stop_dictation":
        stop_dictation()

if __name__ == "__main__":
    main()