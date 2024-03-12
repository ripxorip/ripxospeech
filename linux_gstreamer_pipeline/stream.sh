#!/usr/bin/env bash

if [ "$1" == "--client" ]; then
  # Client
  gst-launch-1.0 -v \
    pulsesrc buffer-time=100000 latency-time=10000 ! \
    opusenc frame-size=5 ! \
    rtpopuspay ! \
    queue max-size-buffers=200 max-size-time=20000000 max-size-bytes=2000 ! \
    udpsink host=100.101.164.159 port=5137 buffer-size=200
elif [ "$1" == "--server" ]; then
  # Server
  gst-launch-1.0 \
    udpsrc port=5137 buffer-size=200 ! \
    application/x-rtp,media=audio,clock-rate=48000,encoding-name=OPUS,payload=96 ! \
    rtpopusdepay ! \
    queue max-size-time=20000000 ! \
    opusdec ! \
    pulsesink
else
  echo "Usage: $0 --server | --client"
fi