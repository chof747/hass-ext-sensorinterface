#!/bin/bash

BASENAME=$(dirname "$0")

FILES=`ls $BASENAME/devices-discovery/*.json`

for device in $FILES; do
    device_id=$(basename "$device" .json)
    echo "$device => homeassistant/sensor/$device_id/config"
    mosquitto_pub -h mqtt -t "homeassistant/sensor/$device_id/config" -f $device
done