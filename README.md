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

### sensor/areas

### sensor/types
