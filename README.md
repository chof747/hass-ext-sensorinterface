# Sensor Interface

Home Assistant custom component providing sensor data in REST format and for low level network protocols.

## Features

- Provides most recent data from sensors attached to home assistant grouped by areas, device type
- Allows REST access to sensors based on entity-id, device class or area
- provides WebSocket services also for sensor data based on device classes, area or entity id
- Allows cycling through sensor groups for easy access for small devices

## API Design & Structure

The API is designed to support small devices which are reading and displaying e.g. the environmental conditions in an apartment and have either minimal or no persistence capabilities and/or cannot follow the events all the time.

*Typical consuming device characteristics*

- Limited storage and computing power (e.g. microcontrollers)
- Limited energy (devices on battery or handheld)
- Limited display capabilities (a small oled or only indicators)
- Limited input and control capabilities (e.g. just a few buttons)

The *major design principles* for the APIs are therefore:

1. Provide suitable grouping of sensors
2. Allow consumers first to learn about the groups and then retrieve the single sensors of a group or the full set
3. Get operations for single sensors enable cycling through the data
4. Data provided in a call contain always the technical IDs as well as the friendly names of the sensors as well as the groups

## API Structure

### sensors/areas

Provides sensor data structured by areas:

#### List the areas

Provides a dictonary of the area ids as keys and the name of the areas as values

The format is like this

```json
[
    "<Id of Area 1>" : "<Name of the area 1>",
    "<Id of Area 2>" : "<Name of area 2>",
    ...
]
```

#### Get the next sensor in an area

Provides the next sensor (ordered by type and name) from the _current_ one. If _current_ is not provided it starts with the first in the order. If _current_ is the last in the ordered list, it proceeds with the first, thus cycling through the sensors in an area

The websocket command for this command is provided in the following form:

```json
    {
        "type" : "sensors/areas/next",
        "area" : "<id of the area",
        "current" : "<id of the current sensor>"

    }
```

- for _current_ the id of the sensor is used. If no id is provided it starts from the beginning
- for _area_ the id of an area needs to be provided

99. The format of a sensor reading is as follows:

```json
{
    "id"    : "<entity id>",
    "name"  : "Friendly Name of the sensor",
    "type"  : "temperature|humidity|pressure|power ...",
    "value" : <Value of the Sensor>,
    "unit"  : "The unit of measurement of the sensor"
}
```

### sensor/types
