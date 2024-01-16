#!/usr/bin/env python

import socket
import sys
import subprocess
import os
import signal
import socket

def main():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    server_address = ('0.0.0.0', 1538)
    sock.bind(server_address)

    stream_process = None
    while True:
        data, address = sock.recvfrom(4096)
        command = data.decode()
        if command == "start":
            if stream_process is None:
                stream_process = subprocess.Popen(["linux_gstreamer_server/serve.sh"], preexec_fn=os.setsid)
        elif command == "stop":
            if stream_process is not None:
                os.killpg(os.getpgid(stream_process.pid), signal.SIGTERM)
                stream_process = None

    sock.close()

if __name__ == "__main__":
    main()
