import argparse
import numpy as np
import sounddevice as sd
import socket
import threading
import time
import wave
import sys
import os

# Set the threshold
threshold = 0.5

# Set buffer size and sample rate
buffer_size = 64  # Adjust as needed
sample_rate = 48000  # Standard for most audio devices

class Server:
    def __init__(self):
        self.has_peak = False
        self.ip_thread_handle = threading.Thread(target=self.ip_thread)
        self.ip_thread_handle.start()
        self.current_recording = []
        with sd.InputStream(callback=self.audio_callback, blocksize=buffer_size, samplerate=sample_rate, channels=1) as stream:
            print("Input latency:", stream.latency*1000, "ms")
            sd.sleep(10000000)

    def audio_callback(self, indata, frames, time, status):
        for s in indata:
            sample = s[0]
            self.current_recording.append(sample)
            if abs(sample) > threshold and not self.has_peak:
                self.has_peak = True
                print("Threshold exceeded")
                # Convert the floating-point numbers to 16-bit integers
                int_samples = (np.array(self.current_recording) * 32767).astype(np.int16)
                # Save the current recording as a wav file using wave
                with wave.open("/tmp/rec.wav", 'w') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)  # Set sample width to 2 bytes for 16-bit audio
                    wf.setframerate(sample_rate)
                    wf.writeframes(int_samples.tobytes())
                # Send threshold exceeded message to client
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                server_address = (self.ip_address, 7822)
                s.sendto(b"threshold_exceeded", server_address)

    def ip_thread(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('0.0.0.0', 7822)
        s.bind(server_address)
        while True:
            data, address = s.recvfrom(4096)
            if data:
                self.ip_address = address[0]
                self.has_peak = False
                self.current_recording = []

class Client:
    def __init__(self, server_ip):
        self.my_peak_time = 0
        self.server_ip = server_ip
        self.has_peak = False

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (self.server_ip, 7822)
        s.sendto(b"start_stream", server_address)

        self.threshold_exceeded_thread_handle = threading.Thread(target=self.threshold_exceeded_thread)
        self.threshold_exceeded_thread_handle.start()

        with sd.InputStream(callback=self.audio_callback, blocksize=buffer_size, samplerate=sample_rate, channels=1) as stream:
            print("Input latency:", stream.latency*1000, "ms")
            sd.sleep(10000000)

    def threshold_exceeded_thread(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('0.0.0.0', 7822)
        s.bind(server_address)
        while True:
            data, address = s.recvfrom(4096)
            # Print the time difference in ms
            print("Time difference:", (time.time() - self.my_peak_time)*1000, "ms")

    def audio_callback(self, indata, frames, _time, status):
        for s in indata:
            sample = s[0]
            if abs(sample) > threshold and not self.has_peak:
                self.has_peak = True
                print("Threshold exceeded")
                # Save the current time
                self.my_peak_time = time.time()

# Get the files by:
# scp ripxorip@voiceboxlinux:/tmp/rec.wav /tmp/rec.wav && vlc /tmp/rec.wav

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=['server', 'client'], help="run as server or client")
    parser.add_argument("--server_ip", help="the server IP address (required if mode is client)")
    args = parser.parse_args()

    if args.mode == 'client' and args.server_ip is None:
        parser.error("--server_ip is required if mode is client")

    if args.mode == 'server':
        server = Server()
    else:
        client = Client(args.server_ip)