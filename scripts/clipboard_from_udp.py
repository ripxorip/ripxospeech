import socket
import subprocess

UDP_IP = "0.0.0.0"
UDP_PORT = 1339

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(8192)
    string = data.decode('utf-8')
    print("received message: %s" % string)
    subprocess.run(['wl-copy', string])
