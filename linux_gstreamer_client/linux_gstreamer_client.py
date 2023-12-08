import gi
import signal
import sys

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

SOUND_SERVER_IP = "100.100.250.30"
GST_SOUND_PORT="5137"

# Initialize GStreamer
Gst.init(None)

# Build the pipeline
pipeline = Gst.parse_launch("pulsesrc buffer-time=100000 latency-time=10000 ! opusenc frame-size=20 ! rtpopuspay ! queue max-size-buffers=200 max-size-time=20000000 max-size-bytes=2000 ! udpsink host={} port={} buffer-size=200 buffer-size=200".format(SOUND_SERVER_IP, GST_SOUND_PORT))

# Start playing
pipeline.set_state(Gst.State.PLAYING)

# Function to handle signal
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    pipeline.set_state(Gst.State.NULL)
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

# Create a GLib Main Loop and run it
mainloop = GLib.MainLoop()
try:
    mainloop.run()
except KeyboardInterrupt:
    mainloop.quit()
    pipeline.set_state(Gst.State.NULL)
