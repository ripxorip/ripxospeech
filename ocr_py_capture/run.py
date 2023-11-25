import argparse
import subprocess
import time
import pytesseract
from PIL import Image, ImageGrab
import threading
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

class GoogleDocsDictation:
    def __init__(self):
        voiceboxclient_ip = ""

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        # event loop
        while True:
            data, addr = sock.recvfrom(1024)
            message = data.decode()
            if message.startswith("start@"):
                voiceboxclient_ip = message.split("@")[1]
                self.start_dictation()
            elif message == "end":
                self.end_dictation()
        # cleanup
        sock.close()

    def switch_to_chrome(self):
        subprocess.run(["xdotool", "search", "--onlyvisible", "--class", "google-chrome", "windowactivate"])

    def start_dictation(self):
        self.switch_to_chrome()
        time.sleep(0.1)
        subprocess.run(["xdotool", "key", "ctrl+a"])
        subprocess.run(["xdotool", "key", "Delete"])
        subprocess.run(["xdotool", "key", "ctrl+shift+s"])

        self.stop_polling = False
        self.poll_thread = threading.Thread(target=self.poll_current_text)
        self.poll_thread.start()

        # Faked stop dictation
        time.sleep(6)
        self.end_dictation()
        self.stop_polling = True
        self.poll_thread.join()

    def get_current_text(self):
        # Capture screenshot of specific region
        screenshot_cropped = ImageGrab.grab(bbox=(240, 210, 1050, 742))
        # Use pytesseract to extract text from the captured screenshot
        text = pytesseract.image_to_string(screenshot_cropped)
        return text

    def poll_current_text(self):
        while not self.stop_polling:
            text = self.get_current_text()
            # FIXME Possibly sleep here to reduce CPU usage
            print(text)

    def end_dictation(self):
        subprocess.run(["xdotool", "key", "Escape"])
        self.get_current_text()

    def test(self):
        self.start_dictation()

def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Tool to use for routing my voice to different speech recognition servers")
    # Add the arguments
    parser.add_argument("-a", "--action", help="The action to perform", choices=["test", "docs"], required=True)
    args = parser.parse_args()

    if args.action == "test":
        google_docs_dictation = GoogleDocsDictation()
        google_docs_dictation.test()
        exit(0)
    elif args.action == "docs":
        google_docs_dictation = GoogleDocsDictation()
        google_docs_dictation.run()
        exit(0)

if __name__ == "__main__":
    main()