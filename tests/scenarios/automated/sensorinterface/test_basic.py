import logging
from .fixtures.websocket import runSocketCommandAndReceiveReturn
from .fixtures import MQTT


LOGGER = logging.getLogger("WEBSOCKET_BASIC")


def test_sensors_list(hassendpoint, MQTT):
    mc = MQTT.reconnect()
    mc.publish("home/sleepingroom/temperature", 26)

    assert runSocketCommandAndReceiveReturn("sensors/list") == {
        "id": 1,
        "type": "result",
        "success": True,
        "result": [
            {
                "id": "sensor.wssr_humd",
                "name": "Luftfeuchtigkeit",
                "area": "Schlafzimmer",
                "type": "humidity",
                "value": "unknown",
            },
            {
                "id": "sensor.wssr_temp",
                "name": "Temperatur",
                "area": "Schlafzimmer",
                "type": "temperature",
                "value": "26",
            },
        ],
    }

    assert True
