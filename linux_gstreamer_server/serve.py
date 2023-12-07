import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

import numpy as np

Gst.init(None)
loop = GObject.MainLoop()

def bus_callback(bus, message, loop):
    print(message.type)
    t = message.type
    if t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(f"Error: {err}, Debug info: {debug}")
        loop.quit()
    elif t == Gst.MessageType.EOS:
        loop.quit()

    return True

def new_sample_callback(appsink, user_data):
    # print("New sample callback")
    sample = appsink.emit("pull-sample")
    if sample:
        #print(sample.get_caps().to_string())
        buffer = sample.get_buffer()
        size = buffer.get_size()
        #print(f"Received buffer with size: {size}")
        data = buffer.extract_dup(0, size)
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Reshape the array to separate the channels
        audio_data = audio_data.reshape(-1, 2)
        channel1 = audio_data[:, 0]
        channel2 = audio_data[:, 1]

        #print(f"Channel 1: {channel1}")
        #print(f"Channel 2: {channel2}")

        # Print the length of channel 1
        #print(f"Length of channel 1: {len(channel1)}")

    return Gst.FlowReturn.OK

GObject.threads_init()

# Create the pipeline
pipeline = Gst.Pipeline()

# Create the elements
src = Gst.ElementFactory.make("udpsrc", "src")
src.set_property("port", 5137)
src.set_property("buffer-size", 200)

caps = Gst.Caps.from_string("application/x-rtp,media=audio,clock-rate=48000,encoding-name=OPUS,payload=96")
filter = Gst.ElementFactory.make("capsfilter", "filter")
filter.set_property("caps", caps)

depay = Gst.ElementFactory.make("rtpopusdepay", "depay")

queue = Gst.ElementFactory.make("queue", "queue")
queue.set_property("max-size-time", 20000000)

dec = Gst.ElementFactory.make("opusdec", "dec")

sink = Gst.ElementFactory.make("appsink", "sink")
sink.set_property("sync", False)
sink.set_property("emit-signals", True)
sink.connect("new-sample", new_sample_callback, None)

# Add elements to the pipeline
for elem in [src, filter, depay, queue, dec, sink]:
    pipeline.add(elem)

# Link the elements
src.link(filter)
filter.link(depay)
depay.link(queue)
queue.link(dec)
dec.link(sink)

# Set up bus callback
bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect("message", bus_callback, loop)

# Start the pipeline
pipeline.set_state(Gst.State.PLAYING)

try:
    loop.run()
except KeyboardInterrupt:
    pass
finally:
    # Cleanup
    pipeline.set_state(Gst.State.NULL)