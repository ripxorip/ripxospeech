class App:
    def __init__(self):
        print("App init")

    def button_clicked(self, button):
        print("button clicked")

    def start_keyboard_server(self):
        print("start_keyboard_server")

    def start_audio_stream(self):
        # Shall start the local gstreamer pipeline
        # and send a message to the gstreamer server to start listening
        print("start_audio_stream")

    def stop_audio_stream(self):
        # Shall stop the local gstreamer pipeline
        # and send a message to the gstreamer server to stop listening
        print("stop_audio_stream")