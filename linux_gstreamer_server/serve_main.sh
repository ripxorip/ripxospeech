#!env bash

echo "Before starting, make sure that the folling is running (tmux on lab):"
echo "1.)  nix develop -c \$SHELL"
echo "2.)  PIPEWIRE_LATENCY="1024/48000" jacktrip -s"
echo "3.)  Make sure Jack is running on Windows VM and:"
echo "     a.)  qjackctl is running"
echo "     b.)  JackTrip is running:"
echo "          .\jacktrip.exe -c 192.168.122.1"
echo "4.)  Gstreamer running on Linux VM:"
echo "     a.)  ./linux_gstreamer_server/serve_dest.sh"
echo "     b.)  gstreamer routed to the virtual microphone (qpwgraph)"
echo "Press enter to continue..."
read

gst-launch-1.0 \
  -vvv \
  udpsrc port=5137 buffer-size=200 ! \
  application/x-rtp,media=audio,clock-rate=48000,encoding-name=OPUS,payload=96 ! \
  tee name=t \
    t. ! queue ! \
        rtpopusdepay ! \
        opusdec ! \
        audioconvert ! \
        jackaudiosink client-name=JackTrip port-names=JackTrip:send_1,JackTrip:send_2 low-latency=true \
    t. ! queue ! \
        udpsink host=192.168.122.137 port=5137