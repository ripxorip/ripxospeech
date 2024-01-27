# This class is used to supervise incoming sentences and preprocess them before sending keystrokes
# it shall also enable the user to undo/redo and editing in line using the voice
import threading

class Doublethink:
    def __init__(self, lang):
        self.lang = lang
        self.chunk_timer = None
        self.current_chunk_buf = []

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

    def chunk_cbk(self):
        print("*Doublethink: chunk_cbk*")
        for keycode, event_type in self.current_chunk_buf:
            self.emit_keyevent(keycode, event_type)

    def set_emit_keyevent(self, emit_keyevent):
        self.emit_keyevent = emit_keyevent