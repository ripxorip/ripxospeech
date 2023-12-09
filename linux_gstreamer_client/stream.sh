#!/bin/bash

gst-launch-1.0 -v \
  pulsesrc buffer-time=100000 latency-time=10000 ! \
  opusenc frame-size=5 ! \
  rtpopuspay ! \
  queue max-size-buffers=200 max-size-time=20000000 max-size-bytes=2000 ! \
  udpsink host=100.100.250.30 port=5137 buffer-size=200
