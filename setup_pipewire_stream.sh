#!/bin/bash

echo "Setting up pa sink"
pactl load-module module-tunnel-sink server=tcp:100.97.216.58:4656
sleep 1
echo "Routing microphone to sink"
pw-link alsa_input.usb-Focusrite_Scarlett_Solo_USB_Y7MAVDU2758A86-00.analog-stereo:capture_FL tunnel-sink.tcp:100.97.216.58:4656:playback_FL
