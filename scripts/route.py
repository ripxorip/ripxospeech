#!/usr/bin/env python

import os
import sys
import subprocess
import argparse

IP_ADDR = {
    "lab": "",
    "engine_talon": "100.97.216.58",
    "engine_win11_swe": "",
    "work": "100.101.164.159",
    "station": "100.121.51.47",
}

CLIENTS = ["work", "station"]
SERVERS = ["lab", "engine_talon", "engine_win11_swe"]

VOICE_BOX_CLIENT_PORT="5000"

GST_SOUND_PORT="5137"

LINUX_USER="ripxorip"
TMUX_SESSION_NAME="ripxospeech"

# gst server example `gst-launch-1.0 -v udpsrc port=1337 caps="application/x-rtp, media=(string)audio, clock-rate=(int)48000, encoding-name=(string)OPUS, payload=(int)96" ! rtpopusdepay ! opusdec ! pulsesink`
# gst client example `gst-launch-1.0 -v pulsesrc ! opusenc ! rtpopuspay ! udpsink host=100.97.216.58 port=1337`

def run_command_over_ssh(command, server):
    ssh = subprocess.Popen(["ssh", "{}@{}".format(LINUX_USER, server), command],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    stderr = ssh.stderr.readlines()
    if stderr != []:
        err = "[Error] "
        for line in stderr:
            err += line.decode("utf-8")
        print(err)
    res = ""
    for line in result:
        res += line.decode("utf-8")
    print(res)
    return res

def run(command, server):
    run_command_over_ssh("tmux send-keys -t {} '{}' C-m".format(TMUX_SESSION_NAME, command), IP_ADDR[server])

def abort_command(server):
    run_command_over_ssh("tmux send-keys -t {} C-c".format(TMUX_SESSION_NAME), IP_ADDR[server])

def verify_tmux_session(server):
    print("Verifying tmux session for {}".format(server))
    sessions = run_command_over_ssh("tmux ls", IP_ADDR[server])
    # check if the session exists in the sessions
    if TMUX_SESSION_NAME in sessions:
        print("Session already exists")
    else:
        print("Spawning a new tmux session")
        run_command_over_ssh("tmux new -d -s {}".format(TMUX_SESSION_NAME), IP_ADDR[server])

def kill():
    for c in CLIENTS:
        if IP_ADDR[c] != "":
            verify_tmux_session(c)
            abort_command(c)
    for s in SERVERS:
        if IP_ADDR[s] != "":
            verify_tmux_session(s)
            abort_command(s)

def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Tool to use for routing my voice to different speech  recognition servers")
    # Add the arguments
    parser.add_argument("-c", "--client", help="The client to use", choices=["work", "station"])
    parser.add_argument("-e", "--engine", help="the speech engine to use", choices=["talon", "win11_swe"])
    parser.add_argument("-k", "--kill", help="Kill all active recognitions", action="store_true")
    # Parse the arguments
    args = parser.parse_args()

    if args.kill:
        kill()

if __name__ == "__main__":
    main()