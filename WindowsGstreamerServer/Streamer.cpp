#include <gst/gst.h>

int main(int argc, char *argv[]) {
    // An example client: gst-launch-1.0 -v pulsesrc buffer-time=100000 latency-time=10000 ! opusenc ! rtpopuspay ! queue max-size-buffers=200 max-size-time=20000000 max-size-bytes=2000 ! udpsink host=100.106.115.19 port=5137 buffer-size=200
    // Initialize GStreamer
    gst_init(&argc, &argv);

    // Enable logging
    gst_debug_set_active(TRUE);
    gst_debug_set_default_threshold(GST_LEVEL_INFO);

    // Create a GStreamer pipeline
    GstElement *pipeline = gst_pipeline_new("audio-pipeline");

    // Create elements
    GstElement *udpsrc = gst_element_factory_make("udpsrc", "udp-source");
    GstElement *capsfilter = gst_element_factory_make("capsfilter", "caps-filter");
    GstElement *rtpopusdepay = gst_element_factory_make("rtpopusdepay", "rtp-opus-depay");
    GstElement *queue = gst_element_factory_make("queue", "queue");
    GstElement *opusdec = gst_element_factory_make("opusdec", "opus-decoder");
    GstElement *audioconvert = gst_element_factory_make("audioconvert", "audio-convert");
    GstElement *audioresample = gst_element_factory_make("audioresample", "audio-resample");
    GstElement *autoaudiosink = gst_element_factory_make("autoaudiosink", "auto-audio-sink");

    // Check if all elements are created successfully
    if (!pipeline || !udpsrc || !capsfilter || !rtpopusdepay || !queue || !opusdec || !audioconvert || !audioresample || !autoaudiosink) {
        g_printerr("Not all elements could be created.\n");
        return -1;
    }

    // Set UDP source properties
    g_object_set(G_OBJECT(udpsrc), "port", 5137, "buffer-size", 200, NULL);
    
    // Set capsfilter properties
    GstCaps *caps = gst_caps_from_string("application/x-rtp,media=(string)audio,clock-rate=(int)48000,encoding-name=(string)OPUS,payload=(int)96");
    g_object_set(G_OBJECT(capsfilter), "caps", caps, NULL);
    gst_caps_unref(caps);

    // Set queue properties
    g_object_set(G_OBJECT(queue), "max-size-time", 20000000, NULL);

    // Build the pipeline
    gst_bin_add_many(GST_BIN(pipeline), udpsrc, capsfilter, rtpopusdepay, queue, opusdec, audioconvert, audioresample, autoaudiosink, NULL);
    gst_element_link_many(udpsrc, capsfilter, rtpopusdepay, queue, opusdec, audioconvert, audioresample, autoaudiosink, NULL);

    // Set the pipeline to the playing state
    gst_element_set_state(pipeline, GST_STATE_PLAYING);
    // After setting the pipeline to the playing state
    GstStateChangeReturn ret = gst_element_set_state(pipeline, GST_STATE_PLAYING);
    if (ret == GST_STATE_CHANGE_FAILURE) {
        g_printerr("Unable to set the pipeline to the playing state.\n");
        gst_object_unref(pipeline);
        return -1;
    } else if (ret == GST_STATE_CHANGE_NO_PREROLL) {
        g_print("Pipeline is live and does not need PREROLL ...\n");
    } else if (ret == GST_STATE_CHANGE_ASYNC) {
        g_print("Pipeline is PREROLLING ...\n");
    } else if (ret == GST_STATE_CHANGE_SUCCESS) {
        g_print("Pipeline is PREROLLED ...\n");
    }

    // Run the main loop
    GstBus *bus = gst_element_get_bus(pipeline);
    GstMessage *msg = gst_bus_timed_pop_filtered(bus, GST_CLOCK_TIME_NONE, static_cast<GstMessageType>(GST_MESSAGE_ERROR | GST_MESSAGE_EOS));

    // Parse the message
    if (msg != NULL) {
        GError *err;
        gchar *debug_info;

        switch (GST_MESSAGE_TYPE(msg)) {
            case GST_MESSAGE_ERROR:
                gst_message_parse_error(msg, &err, &debug_info);
                g_printerr("Error received from element %s: %s\n", GST_OBJECT_NAME(msg->src), err->message);
                g_printerr("Debugging information: %s\n", debug_info ? debug_info : "none");
                g_clear_error(&err);
                g_free(debug_info);
                break;
            case GST_MESSAGE_EOS:
                g_print("End-Of-Stream reached.\n");
                break;
            default:
                // Unexpected message
                g_printerr("Unexpected message received.\n");
                break;
        }

        gst_message_unref(msg);
    }

    // Free resources
    gst_object_unref(bus);
    gst_element_set_state(pipeline, GST_STATE_NULL);
    gst_object_unref(pipeline);

    return 0;
}