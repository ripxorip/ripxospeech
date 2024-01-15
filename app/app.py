import subprocess
import os
import signal

class App:
    def __init__(self):
        self.stream_process = None

    def button_clicked(self, button):
        print("button clicked")

    def start_keyboard_server(self):
        print("start_keyboard_server")

    def start_audio_stream(self):
        # Shall start the local gstreamer pipeline
        # and send a message to the gstreamer server to start listening
        # Set os.setsid() to make it run in a new process group,
        # that way we can kill the entire process group when we want to stop the stream
        self.stream_process = subprocess.Popen(["linux_gstreamer_client/stream.sh"], preexec_fn=os.setsid)

    def stop_audio_stream(self):
        # Shall stop the local gstreamer pipeline
        # and send a message to the gstreamer server to stop listening
        if self.stream_process is not None:
            os.killpg(os.getpgid(self.stream_process.pid), signal.SIGINT)
            self.stream_process = None