import logging
from numpy import array

from .fixtures.sensor_stub import SensorStubClass, SensorStubs
from .fixtures.websocket import runSocketCommandAndReceiveReturn

LOGGER = logging.getLogger("AREA_TEST")

# **************************************************************************************
def test_sensors_areas(sockets, hassendpoint):
    result = runSocketCommandAndReceiveReturn("sensors/areas")
    assert result["result"] == {
        "wohnzimmer": "Wohnzimmer",
        "kuche": "Küche",
        "schlafzimmer": "Schlafzimmer",
    }


# **************************************************************************************
def setupSensors1(sst: SensorStubClass) -> array:
    sensor_ids = [
        sst.create_sensor(
            "wslr_temp", "Temperature Living Room", "temperature", "°C", "wohnzimmer"
        ),
        sst.create_sensor(
            "wslr_humd", "Humidity Living Room", "humidity", "%", "wohnzimmer"
        ),
        sst.create_sensor(
            "wslr_airp", "Air Pressure Living Room", "pressure", "mbar", "wohnzimmer"
        ),
        sst.create_sensor(
            "wslr_tmp2", "Laptop inner Temperature", "temperature", "°C", "wohnzimmer"
        ),
    ]

    LOGGER.debug(sensor_ids)

    sst.update_state(sensor_ids[0], 21.7)
    sst.update_state(sensor_ids[1], 44.2)
    sst.update_state(sensor_ids[2], 1014.12)
    sst.update_state(sensor_ids[3], 34.5)

    return sensor_ids


# **************************************************************************************
def test_sensors_areas_next(sockets, hassendpoint, SensorStubs):
    sensor_ids = setupSensors1(SensorStubs)

    result = runSocketCommandAndReceiveReturn(
        "sensors/areas/next", {"area": "wohnzimmer"}
    )

    assert result != False
    assert result["result"] == {
        "name": "Humidity Living Room",
        "type": "humidity",
        "value": "44.2",
        "unit": "%",
        "id": "sensor.wslr_humd",
    }

    result = runSocketCommandAndReceiveReturn(
        "sensors/areas/next", {"area": "wohnzimmer", "current": result["result"]["id"]}
    )

    assert result != False
    assert result["result"] == {
        "name": "Air Pressure Living Room",
        "type": "pressure",
        "value": "1014.12",
        "unit": "mbar",
        "id": "sensor.wslr_airp",
    }

    result = runSocketCommandAndReceiveReturn(
        "sensors/areas/next", {"area": "wohnzimmer", "current": result["result"]["id"]}
    )

    assert result != False
    assert result["result"] == {
        "name": "Laptop inner Temperature",
        "type": "temperature",
        "value": "34.5",
        "unit": "°C",
        "id": "sensor.wslr_tmp2",
    }

    result = runSocketCommandAndReceiveReturn(
        "sensors/areas/next", {"area": "wohnzimmer", "current": result["result"]["id"]}
    )

    assert result != False
    assert result["result"] == {
        "name": "Temperature Living Room",
        "type": "temperature",
        "value": "21.7",
        "unit": "°C",
        "id": "sensor.wslr_temp",
    }

    result = runSocketCommandAndReceiveReturn(
        "sensors/areas/next", {"area": "wohnzimmer", "current": result["result"]["id"]}
    )

    assert result != False
    assert result["result"] == {
        "name": "Humidity Living Room",
        "type": "humidity",
        "value": "44.2",
        "unit": "%",
        "id": "sensor.wslr_humd",
    }


# **************************************************************************************
def test_sensors_areas_prev(sockets, hassendpoint, SensorStubs):
    sensor_ids = setupSensors1(SensorStubs)

    result = runSocketCommandAndReceiveReturn(
        "sensors/areas/prev", {"area": "wohnzimmer"}
    )

    assert result != False
    assert result["result"] == {
        "name": "Temperature Living Room",
        "type": "temperature",
        "value": "21.7",
        "unit": "°C",
        "id": "sensor.wslr_temp",
    }

    result = runSocketCommandAndReceiveReturn(
        "sensors/areas/prev", {"area": "wohnzimmer", "current": result["result"]["id"]}
    )

    assert result != False
    assert result["result"] == {
        "name": "Laptop inner Temperature",
        "type": "temperature",
        "value": "34.5",
        "unit": "°C",
        "id": "sensor.wslr_tmp2",
    }

    result = runSocketCommandAndReceiveReturn(
        "sensors/areas/prev", {"area": "wohnzimmer", "current": result["result"]["id"]}
    )
    assert result != False
    assert result["result"] == {
        "name": "Air Pressure Living Room",
        "type": "pressure",
        "value": "1014.12",
        "unit": "mbar",
        "id": "sensor.wslr_airp",
    }

    result = runSocketCommandAndReceiveReturn(
        "sensors/areas/prev", {"area": "wohnzimmer", "current": result["result"]["id"]}
    )
    assert result != False
    assert result["result"] == {
        "name": "Humidity Living Room",
        "type": "humidity",
        "value": "44.2",
        "unit": "%",
        "id": "sensor.wslr_humd",
    }

    result = runSocketCommandAndReceiveReturn(
        "sensors/areas/prev", {"area": "wohnzimmer", "current": result["result"]["id"]}
    )
    assert result != False
    assert result["result"] == {
        "name": "Temperature Living Room",
        "type": "temperature",
        "value": "21.7",
        "unit": "°C",
        "id": "sensor.wslr_temp",
    }

