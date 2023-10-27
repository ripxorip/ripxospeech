#!/bin/bash

TALON_SERVER_ADDR="100.97.216.58:4656"

WORK_CLIENT_ADDR="100.101.164.159"
STATION_CLIENT_ADDR=""

LINUX_USER="ripxorip"

# Define functions for each target
function setup_work {
    echo "Setting up work"
}

function setup_station {
    echo "Setting up station"
}

function stop_all {
    echo "Stopping all"
}

function stop_work {
    echo "Stopping work"
    ssh $LINUX_USER@$WORK_CLIENT_ADDR "pactl unload-module \$(pactl list short modules | awk -F'\t' '/server=/ {id=\$1} END {print id}')"
}

function stop_station {
    echo "Stopping station"
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
    exit 1
fi