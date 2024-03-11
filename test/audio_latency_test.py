import argparse
import numpy as np
import sounddevice as sd
import socket
import threading
import time
import sys
import os

# Set the threshold
threshold = 0.8

# Define the callback function
def callback(indata, frames, time, status):
    for s in indata:
        sample = s[0]
        if abs(sample) > threshold:
            print("Threshold exceeded")

# Set buffer size and sample rate
buffer_size = 64  # Adjust as needed
sample_rate = 48000  # Standard for most audio devices

class Server:
    def __init__(self):
        self.has_peak = False
        self.ip_thread_handle = threading.Thread(target=self.ip_thread)
        self.ip_thread_handle.start()
        with sd.InputStream(callback=self.audio_callback, blocksize=buffer_size, samplerate=sample_rate, channels=1) as stream:
            sd.sleep(10000)
            print("Input latency:", stream.latency*1000, "ms")

    def audio_callback(self, indata, frames, time, status):
        for s in indata:
            sample = s[0]
            if abs(sample) > threshold and not self.has_peak:
                self.has_peak = True
                print("Threshold exceeded")
                # Send threshold exceeded message to client
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                server_address = (self.ip_address, 7822)
                s.sendto(b"threshold_exceeded", server_address)

    def ip_thread(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('localhost', 7822)
        s.bind(server_address)
        while True:
            data, address = s.recvfrom(4096)
            print('received {} bytes from {}'.format(len(data), address))
            print(data)
            print(address)
            if data:
                print(data.decode('utf-8'))
                print('IP address:', address[0])
                self.ip_addrrss = address[0]
                self.has_peak = False

class Client:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.has_peak = False

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (self.server_ip, 7822)
        s.sendto(b"start_stream", server_address)

        self.threshold_exceeded_thread_handle = threading.Thread(target=self.threshold_exceeded_thread)
        self.threshold_exceeded_thread_handle.start()

        with sd.InputStream(callback=self.audio_callback, blocksize=buffer_size, samplerate=sample_rate, channels=1) as stream:
            sd.sleep(10000)
            print("Input latency:", stream.latency*1000, "ms")

    def threshold_exceeded_thread(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('localhost', 7822)
        s.bind(server_address)
        while True:
            data, address = s.recvfrom(4096)
            print('received {} bytes from {}'.format(len(data), address))
            print(data)
            print(address)

    def audio_callback(self, indata, frames, time, status):
        for s in indata:
            sample = s[0]
            if abs(sample) > threshold and not self.has_peak:
                self.has_peak = True
                print("Threshold exceeded")

# FIXME Also save some audio and send back to verify that the quality was ok somehow!

def main(mode, server_ip=None):
    if mode == 'server':
        # Server code here
        pass
    elif mode == 'client':
        # Client code here
        pass
        with sd.InputStream(callback=callback, blocksize=buffer_size, samplerate=sample_rate, channels=1) as stream:
            print("Input latency:", stream.latency*1000, "ms")
            sd.sleep(10000)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=['server', 'client'], help="run as server or client")
    parser.add_argument("--server_ip", help="the server IP address (required if mode is client)")
    args = parser.parse_args()

    if args.mode == 'client' and args.server_ip is None:
        parser.error("--server_ip is required if mode is client")

    main(args.mode, args.server_ip)
