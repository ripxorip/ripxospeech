# This class is used to supervise incoming sentences and preprocess them before sending keystrokes
# it shall also enable the user to undo/redo and editing in line using the voice
import threading

from collections import deque

import time

from keyboard_server.keycodes import *
from keyboard_server.utils import *

class Doublethink:
    def __init__(self, lang):
        self.lang = lang
        self.chunk_timer = None
        self.current_chunk_buf = []
        self.history = deque(maxlen=100)

    def arm(self):
        # A new invocation of the dictation engine is about to start
        pass

    def reset_timer(self):
        if self.chunk_timer:
            self.chunk_timer.cancel()
        self.chunk_timer = threading.Timer(0.1, self.chunk_cbk)
        self.chunk_timer.start()

    def stop_timer(self):
        if self.chunk_timer:
            self.chunk_timer.cancel()

    def handle_keyevent(self, keycode, event_type):
        self.reset_timer()
        self.current_chunk_buf.append((keycode, event_type))

    def undo(self):
        latest = self.history[-1]
        latest_len = len(latest)
        for i in range(latest_len):
            self.emit_keyevent(get_x11_keycode_from_name('KEY_BACKSPACE'), 0)
            time.sleep(0.01)
            self.emit_keyevent(get_x11_keycode_from_name('KEY_BACKSPACE'), 1)
            time.sleep(0.01)

    def redo(self):
        print("Redoing")

    def chunk_cbk(self):
        text = convert_chunk_to_text(self.current_chunk_buf)
        self.history.append(text)
        chunk = convert_text_to_chunk(text)
        for keycode, event_type in chunk:
            self.emit_keyevent(keycode, event_type)
        self.current_chunk_buf = []

    def set_emit_keyevent(self, emit_keyevent):
        self.emit_keyevent = emit_keyevent