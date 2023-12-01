#!/bin/bash

gst-launch-1.0 udpsrc port=5137 buffer-size=200 ! application/x-rtp,media=audio,clock-rate=48000,encoding-name=OPUS,payload=96 ! rtpopusdepay ! queue max-size-time=20000000 ! opusdec ! pulsesink