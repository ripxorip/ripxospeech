#!/usr/bin/env python

import subprocess
import argparse
import socket

IP_ADDR = {
    "lab": "100.100.250.30",
    "engine_talon": "100.97.216.58",
    "engine_win11_swe": "100.106.115.19",
    "work": "100.101.164.159",
    "station": "100.121.51.47",
}

CLIENTS = ["work", "station"]
SERVERS = ["lab", "engine_talon", "engine_win11_swe"]

VOICE_BOX_CLIENT_PORT="5000"

GST_SOUND_PORT="5137"

LINUX_USER="ripxorip"
TMUX_SESSION_NAME="ripxospeech"

def run_command_over_ssh(command, server):
    print("Running command: {} on {}".format(command, server))
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

def start_gst_server(server):
    run("gst-launch-1.0 -v udpsrc port={} caps=\"application/x-rtp, media=(string)audio, clock-rate=(int)48000, encoding-name=(string)OPUS, payload=(int)96\" ! rtpopusdepay ! opusdec ! pulsesink".format(GST_SOUND_PORT), server)

def route_gst_client(client, server):
    print("Routing gst client from {} to {}".format(client, server))
    run("gst-launch-1.0 -v pulsesrc ! opusenc ! rtpopuspay ! udpsink host={} port={}".format(IP_ADDR[server], GST_SOUND_PORT), client)

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
            run_command_over_ssh("rm ~/dev/x11_keysender/client.txt", IP_ADDR[s])

def setup_talon(server, client):
    print("Setting up talon")
    start_gst_server(server)
    run_command_over_ssh("echo -e 'server_ip={}\nserver_port={}' > ~/dev/x11_keysender/client.txt".format(IP_ADDR[client], VOICE_BOX_CLIENT_PORT), IP_ADDR[server])
    route_gst_client(client, server)

def send_udp_string(server, string):
    # Convert the string to bytes
    bytes = string.encode('utf-8')
    # Send the specified bytes to the specified server over UDP using socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes, (IP_ADDR[server], int(VOICE_BOX_CLIENT_PORT)))

def setup_win11_swe(client):
    server = "lab"
    start_gst_server(server)
    route_gst_client(client, server)

    # FIXME Not sure that all of these are needed
    run_command_over_ssh("pw-link -d alsa_output.pci-0000_08_00.1.hdmi-stereo-extra1:monitor_FL Win11SweGenuine:input_FL", IP_ADDR[server])
    run_command_over_ssh("pw-link -d alsa_output.pci-0000_08_00.1.hdmi-stereo-extra1:monitor_FR Win11SweGenuine:input_FR", IP_ADDR[server])

    run_command_over_ssh("pw-link -d Win11SweGenuine:output_FL alsa_output.pci-0000_08_00.1.hdmi-stereo-extra1:playback_FL", IP_ADDR[server])
    run_command_over_ssh("pw-link -d Win11SweGenuine:output_FR alsa_output.pci-0000_08_00.1.hdmi-stereo-extra1:playback_FR", IP_ADDR[server])

    run_command_over_ssh("pw-link -d gst-launch-1.0:output_FL alsa_output.pci-0000_08_00.1.hdmi-stereo-extra1:playback_FL", IP_ADDR[server])
    run_command_over_ssh("pw-link -d gst-launch-1.0:output_FR alsa_output.pci-0000_08_00.1.hdmi-stereo-extra1:playback_FR", IP_ADDR[server])

    run_command_over_ssh("pw-link -d Win11SweGenuine:input_FR alsa_output.pci-0000_08_00.1.hdmi-stereo-extra1:monitor_FR", IP_ADDR[server])
    run_command_over_ssh("pw-link -d Win11SweGenuine:input_FL alsa_output.pci-0000_08_00.1.hdmi-stereo-extra1:monitor_FL", IP_ADDR[server])

    # This one actually routes the audio to the Windows VM
    run_command_over_ssh("pw-link gst-launch-1.0:output_FL Win11SweGenuine:input_FL", IP_ADDR[server])

    print("hint: To manually verify that the routing is correct: run the following command: pw-link -I -l")

def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Tool to use for routing my voice to different speech recognition servers")
    # Add the arguments
    parser.add_argument("-a", "--action", help="The action to perform", choices=["kill", "route", "win11_start_dictation", "win11_stop_dictation"], required=True)
    parser.add_argument("-c", "--client", help="The client to use", choices=["work", "station"])
    parser.add_argument("-e", "--engine", help="the speech engine to use", choices=["talon", "win11_swe"])
    parser.add_argument("-k", "--kill", help="Kill all active recognitions", action="store_true")
    # Parse the arguments
    args = parser.parse_args()

    if args.action == "kill":
        kill()
        exit(0)
    elif args.action == "route":
        if args.engine is None:
            print("Please specify an engine")
            exit(1)
        elif args.engine == "talon":
            setup_talon("engine_talon", args.client)
        elif args.engine == "win11_swe":
            setup_win11_swe(args.client)
    elif args.action == "win11_start_dictation":
        send_udp_string("engine_win11_swe", "start")
    elif args.action == "win11_stop_dictation":
        send_udp_string("engine_win11_swe", "stop")

if __name__ == "__main__":
    main()