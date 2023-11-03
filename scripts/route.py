#!/usr/bin/env python

import os
import sys
import subprocess
import argparse

IP_ADDR = {
    "lab": "",
    "engine_talon": "100.97.216.58",
    "engine_win11_swe": "",
    "voice_box_work": "100.101.164.159",
    "voice_box_station": "100.121.51.47",
}

VOICE_BOX_CLIENT_PORT="5000"

GST_SOUND_PORT="5137"

LINUX_USER="ripxorip"
TMUX_SESSION_NAME="ripxospeech"

def run_command_over_ssh(command, server):
    ssh = subprocess.Popen(["ssh", "{}@{}".format(LINUX_USER, server), command],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    res = ""
    for line in result:
        res += line.decode("utf-8")
    print(res)
    return res

def run_command_in_tmux_session(command, server):
    pass

def verify_tmux_session(server):
    sessions = run_command_over_ssh("tmux ls", IP_ADDR[server])
    # check if the session exists in the sessions
    if TMUX_SESSION_NAME in sessions:
        return
    else:
        run_command_over_ssh("tmux new -d -s {}".format(TMUX_SESSION_NAME), IP_ADDR[server])

def kill():
    pass

def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Tool to use for routing my voice to different speech  recognition servers")
    # Add the arguments
    parser.add_argument("-s", "--server", help="The target server to route to", choices=["work", "station", "none"])
    parser.add_argument("-e", "--engine", help="the speech engine to use", choices=["talon", "win11_swe"])
    parser.add_argument("-k", "--kill", help="kill the server", action="store_true")
    # Parse the arguments
    args = parser.parse_args()
    if args.kill:
        verify_tmux_session("voice_box_work")
        print("Killing the server")
    server = args.server
    engine = args.engine


if __name__ == "__main__":
    main()