import gi
import signal
import sys

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

IP_ADDR = {
    "lab": "100.100.250.30",
    "engine_talon": "100.97.216.58",
    "engine_win11_swe": "100.106.115.19",
    "work": "100.101.164.159",
    "station": "100.121.51.47",
}

CLIENTS = ["work", "station"]
SERVERS = ["lab", "engine_talon", "engine_win11_swe"]

VOICE_BOX_CLIENT_PORT="5000"

GST_SOUND_PORT="5137"
# Initialize GStreamer
Gst.init(None)

# Build the pipeline
pipeline = Gst.parse_launch("pulsesrc buffer-time=100000 latency-time=10000 ! opusenc ! rtpopuspay ! queue max-size-buffers=200 max-size-time=20000000 max-size-bytes=2000 ! multiudpsink clients={}:{},{}:{} buffer-size=200".format(IP_ADDR["engine_talon"], GST_SOUND_PORT, IP_ADDR["engine_win11_swe"], GST_SOUND_PORT))

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
