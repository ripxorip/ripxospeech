import argparse
import subprocess
import time
import pytesseract
from PIL import Image, ImageGrab
import threading
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

class KeyPresser:
    def __init__(self, test=False):
        self.test = test
        self.charToKeyCombo = {
            "esc": 0x09,
            "1": 0x0A,
            "2": 0x0B,
            "3": 0x0C,
            "4": 0x0D,
            "5": 0x0E,
            "6": 0x0F,
            "7": 0x10,
            "8": 0x11,
            "9": 0x12,
            "0": 0x13,
            "minus": 0x14,
            "equal": 0x15,
            "backspace": 0x16,
            "tab": 0x17,
            "q": 0x18,
            "w": 0x19,
            "e": 0x1A,
            "r": 0x1B,
            "t": 0x1C,
            "y": 0x1D,
            "u": 0x1E,
            "i": 0x1F,
            "o": 0x20,
            "p": 0x21,
            "leftbrace": 0x22,
            "rightbrace": 0x23,
            "enter": 0x24,
            "leftctrl": 0x25,
            "a": 0x26,
            "s": 0x27,
            "d": 0x28,
            "f": 0x29,
            "g": 0x2A,
            "h": 0x2B,
            "j": 0x2C,
            "k": 0x2D,
            "l": 0x2E,
            "semicolon": 0x2F,
            "apostrophe": 0x30,
            "grave": 0x31,
            "leftshift": 0x32,
            "backslash": 0x33,
            "z": 0x34,
            "x": 0x35,
            "c": 0x36,
            "v": 0x37,
            "b": 0x38,
            "n": 0x39,
            "m": 0x3A,
            ",": 0x3B,
            ".": 0x3C,
            "/": 0x3D,
            "rightshift": 0x3E,
            "kpasterisk": 0x3F,
            "leftalt": 0x40,
            " ": 0x41,
            "capslock": 0x42,
            "f1": 0x43,
            "f2": 0x44,
            "f3": 0x45,
            "f4": 0x46,
            "f5": 0x47,
            "f6": 0x48,
            "f7": 0x49,
            "f8": 0x4A,
            "f9": 0x4B,
            "f10": 0x4C,
            "numlock": 0x4D,
            "scrolllock": 0x4E,
            "kp7": 0x4F,
            "kp8": 0x50,
            "kp9": 0x51,
            "kpminus": 0x52,
            "kp4": 0x53,
            "kp5": 0x54,
            "kp6": 0x55,
            "kpplus": 0x56,
            "kp1": 0x57,
            "kp2": 0x58,
            "kp3": 0x59,
            "kp0": 0x5A,
            "kpdot": 0x5B,
            "zenkakuhankaku": 0x5D,
            "102nd": 0x5E,
            "f11": 0x5F,
            "f12": 0x60,
            "ro": 0x61,
            "katakana": 0x62,
            "hiragana": 0x63,
            "henkan": 0x64,
            "katakanahiragana": 0x65,
            "muhenkan": 0x66,
            "kpjpcomma": 0x67,
            "kpenter": 0x68,
            "rightctrl": 0x69,
            "kpslash": 0x6A,
            "sysrq": 0x6B,
            "rightalt": 0x6C,
            "linefeed": 0x6D,
            "home": 0x6E,
            "up": 0x6F,
            "pageup": 0x70,
            "left": 0x71,
            "right": 0x72,
            "end": 0x73,
            "down": 0x74,
            "pagedown": 0x75,
            "insert": 0x76,
            "delete": 0x77,
            "macro": 0x78,
            "mute": 0x79,
            "volumedown": 0x7A,
            "volumeup": 0x7B,
            "power": 0x7C,
            "kpequal": 0x7D,
            "kpplusminus": 0x7E,
            "pause": 0x7F,
            "scale": 0x80,
            "kpcomma": 0x81,
            "hanguel": 0x82,
            "hanja": 0x83,
            "yen": 0x84,
            "leftmeta": 0x85,
            "rightmeta": 0x86,
            "compose": 0x87,
            "\n": 0x24,
            "å": 0x00,
            "ä": 0x00,
            "ö": 0x00,
            "?": 0x00,
            "!": 0x00
        } 
        self.voiceboxclient_ip = ""

    def reset(self):
        self.sent_text = ""

    def process_key(self, key):
        if key in self.charToKeyCombo:
            if self.charToKeyCombo[key] != 0x00:
                # Get the key code
                keyCode = self.charToKeyCombo[key]
                self.send_key(keyCode, True)
                self.send_key(keyCode, False)
                return

        c = key[0]

        # Check if c is upper case
        upper = c.isupper()
        if upper:
            self.send_key(self.charToKeyCombo["leftshift"], True)

        # Convert c to lower case
        c = c.lower()

        # Handle the special keys
        if c == 'ö':
            self.send_key(self.charToKeyCombo["rightalt"], True)
            self.send_key(self.charToKeyCombo["o"], True)
            self.send_key(self.charToKeyCombo["o"], False)
            self.send_key(self.charToKeyCombo["rightalt"], False)
        elif c == 'å':
            self.send_key(self.charToKeyCombo["rightalt"], True)
            self.send_key(self.charToKeyCombo["a"], True)
            self.send_key(self.charToKeyCombo["a"], False)
            self.send_key(self.charToKeyCombo["rightalt"], False)
        elif c == 'ä':
            self.send_key(self.charToKeyCombo["rightalt"], True)
            self.send_key(self.charToKeyCombo["r"], True)
            self.send_key(self.charToKeyCombo["r"], False)
            self.send_key(self.charToKeyCombo["rightalt"], False)
        elif c == '?':
            self.send_key(self.charToKeyCombo["leftshift"], True)
            self.send_key(self.charToKeyCombo["/"], True)
            self.send_key(self.charToKeyCombo["/"], False)
            self.send_key(self.charToKeyCombo["leftshift"], False)
        elif c == '!':
            self.send_key(self.charToKeyCombo["leftshift"], True)
            self.send_key(self.charToKeyCombo["1"], True)
            self.send_key(self.charToKeyCombo["1"], False)
            self.send_key(self.charToKeyCombo["leftshift"], False)
        else:
            # Get the key code
            keyCode = self.charToKeyCombo[c]
            self.send_key(keyCode, True)
            self.send_key(keyCode, False)

        if upper:
            self.send_key(self.charToKeyCombo["leftshift"], False)

        return

    def send_key(self, key, press):
        press = not press
        if self.test:
            # Get the name of the key from the self.charToKeyCombo dict
            key_name = ""
            for k, v in self.charToKeyCombo.items():
                if v == key:
                    key_name = k
            if press:
                print("Pressing key:", key_name)
            else:
                print("Releasing key:", key_name)
        else:
            # Create a string with key as hex, 1 or 0 for press or release
            message = "{:02X},{}".format(key, int(press))
            if self.voiceboxclient_ip != "":
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(message.encode(), (self.voiceboxclient_ip, 5000))
                sock.close()
                # FIXME tune this delay (Might need to be longer)
                time.sleep(0.01)
    
    def handle_text_change(self, input_text):
        # Remove the last \n if it exists (strip from tesseract output)
        #
        #
        if input_text.endswith("\n"):
            input_text = input_text[:-1]

        # Add whitespace after each newline
        #
        #
        input_text = input_text.replace("\n", " \n")

        # FIXME remove this when I have a better solution for newlines altogether (For now they are removed)
        input_text = input_text.replace("\n", "")

        # Remove chars that are not in the charToKeyCombo dict
        #
        #
        og_input_text = input_text
        input_text = "".join([c for c in input_text if c.lower() in self.charToKeyCombo])
        # Print the removed chars
        removed_chars = ""
        for c in og_input_text:
            if c not in input_text:
                removed_chars += c

        if removed_chars != "":
            print("Got unsupported chars:", removed_chars)

        # Find out what has been sent
        #
        #
        num_identical_chars = 0
        diff = 0
        for i in range(0, len(input_text)):
            if len(self.sent_text) > i:
                if self.sent_text[i] != input_text[i]:
                    # delete all chars from i to end of sent_text
                    diff = len(self.sent_text) - i
                    self.sent_text = self.sent_text[:i]
                    break
                else:
                    num_identical_chars += 1

        # Remove the chars that are not identical
        #
        #
        if diff > 0:
            for i in range(0, diff):
                self.process_key("backspace")

        # Send the remaining chars
        for i in range(num_identical_chars, len(input_text)):
            self.process_key(input_text[i])
            self.sent_text += input_text[i]

class GoogleDocsDictation:
    def __init__(self, test=False):
        self.test = test
        self.kp = KeyPresser(test=test)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        # event loop
        while True:
            data, addr = sock.recvfrom(1024)
            message = data.decode()
            if message.startswith("start@"):
                self.kp.voiceboxclient_ip = message.split("@")[1]
                self.start_dictation()
            elif message == "stop":
                self.end_dictation()
                self.running = False
                self.poll_thread.join()
        # cleanup
        sock.close()

    def unittest(self):
        self.kp.reset()
        # Read the test data from file
        test_data = []
        with open("test_input.txt", "r") as f:
            for line in f:
                # Remove the surrounding quotes
                line = line[1:-3]
                print(line)
                test_data.append(line[:-1])

        for i in range(len(test_data)):
            print("*** Sending:", test_data[i])
            self.kp.handle_text_change(test_data[i])

    def switch_to_chrome(self):
        subprocess.run(["xdotool", "search", "--onlyvisible", "--class", "google-chrome", "windowactivate"])

    def start_dictation(self):
        self.kp.reset()
        self.switch_to_chrome()
        time.sleep(0.1)
        subprocess.run(["xdotool", "key", "ctrl+a"])
        subprocess.run(["xdotool", "key", "Delete"])
        subprocess.run(["xdotool", "key", "ctrl+shift+s"])

        self.running = True
        self.poll_thread = threading.Thread(target=self.poll_current_text)
        self.poll_thread.start()

    def get_current_text(self, save_screenshot=False):
        # Capture screenshot of specific region
        screenshot_cropped = ImageGrab.grab(bbox=(210, 130, 1030, 753))
        if save_screenshot:
            screenshot_cropped.save("screenshot.png")
            # Also save the full screenshot
            screenshot_full = ImageGrab.grab()
            screenshot_full.save("screenshot_full.png")
        # Use pytesseract to extract text from the captured screenshot
        text = pytesseract.image_to_string(screenshot_cropped)
        if text == "B Meetingnotes &% Emaildraftt @ More\n":
            return ""
        return text

    def poll_current_text(self):
        while self.running:
            if self.test:
                text = self.get_current_text()
                formatted_text = repr(text)[1:-1].replace("\\n", r"\n").replace("\\t", r"\t")
                print("\"{}\",".format(formatted_text))
            else:
                text = self.get_current_text()
                self.kp.handle_text_change(text)

    def end_dictation(self):
        subprocess.run(["xdotool", "key", "Escape"])

    def test(self):
        self.start_dictation()

def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Tool to use for routing my voice to different speech recognition servers")
    # Add the arguments
    parser.add_argument("-a", "--action", help="The action to perform", choices=["unittest", "log", "docs"], required=True)
    args = parser.parse_args()

    if args.action == "unittest":
        google_docs_dictation = GoogleDocsDictation(test=True)
        google_docs_dictation.unittest()
        exit(0)
    elif args.action == "log":
        google_docs_dictation = GoogleDocsDictation(test=True)
        google_docs_dictation.run()
        exit(0)
    elif args.action == "docs":
        google_docs_dictation = GoogleDocsDictation()
        google_docs_dictation.run()
        exit(0)

if __name__ == "__main__":
    main()