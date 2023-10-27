#!/bin/bash

TALON_SERVER_ADDR="100.97.216.58"
TALON_SERVER_PORT="4656"

WORK_CLIENT_ADDR="100.101.164.159"
STATION_CLIENT_ADDR="100.121.51.47"

CLIENT_PORT="5000"

LINUX_USER="ripxorip"

# Define functions for each target
function setup_work {
    ssh $LINUX_USER@$TALON_SERVER_ADDR "echo -e 'server_ip=$WORK_CLIENT_ADDR\nserver_port=$CLIENT_PORT' > ~/dev/x11_keysender/client.txt"
    ssh $LINUX_USER@$WORK_CLIENT_ADDR "pactl load-module module-tunnel-sink server=tcp:$TALON_SERVER_ADDR:$TALON_SERVER_PORT"
    sleep 1
    ssh $LINUX_USER@$WORK_CLIENT_ADDR "pw-link alsa_input.usb-Focusrite_Scarlett_Solo_USB_Y7MAVDU2758A86-00.analog-stereo:capture_FL tunnel-sink.tcp:$TALON_SERVER_ADDR:$TALON_SERVER_PORT:playback_FL"
}

function setup_station {
    ssh $LINUX_USER@$TALON_SERVER_ADDR "echo -e 'server_ip=$STATION_CLIENT_ADDR\nserver_port=$CLIENT_PORT' > ~/dev/x11_keysender/client.txt"
    ssh $LINUX_USER@$STATION_CLIENT_ADDR "pactl load-module module-tunnel-sink server=tcp:$TALON_SERVER_ADDR:$TALON_SERVER_PORT"
    sleep 1
    ssh $LINUX_USER@$STATION_CLIENT_ADDR "pw-link alsa_input.usb-Focusrite_Scarlett_6i6_USB_00003367-00.analog-surround-21:capture_FL tunnel-sink.tcp:$TALON_SERVER_ADDR:$TALON_SERVER_PORT:playback_FL"
}

function stop_all {
    stop_station
    stop_work
    ssh $LINUX_USER@$TALON_SERVER_ADDR "rm ~/dev/x11_keysender/client.txt"
}

function stop_work {
    ssh $LINUX_USER@$WORK_CLIENT_ADDR "pactl unload-module \$(pactl list short modules | awk -F'\t' '/server=/ {id=\$1} END {print id}')"
}

function stop_station {
    ssh $LINUX_USER@$STATION_CLIENT_ADDR "pactl unload-module \$(pactl list short modules | awk -F'\t' '/server=/ {id=\$1} END {print id}')"
}

# Parse command line arguments
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    --target)
    target="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    shift # past argument
    ;;
esac
done

# Check for missing parameters
if [ -z "$target" ]; then
    echo "Usage: $0 --target [work|station|none]"
    exit 1
fi

# Set client configuration based on target
if [ "$target" == "work" ]; then
    stop_station
    setup_work
elif [ "$target" == "station" ]; then
    stop_work
    setup_station
elif [ "$target" == "none" ]; then
    stop_all
else
    echo "Invalid target: $target"
    echo "Usage: $0 --target [work|station|none]"
    exit 1
fi