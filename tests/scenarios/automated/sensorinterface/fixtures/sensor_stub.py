from array import array
from .websocket import runSocketCommandAndReceiveReturn
from .mqtt import MQTT, MqttFixture

import string
import random
import pytest
import logging

LOGGER = logging.getLogger("SensorStubs")


class SensorStubClass(object):
    def __init__(self):
        self.sensors = {}

    def _assignSensorToArea(self, sensor_id: str, area: str):
        result = runSocketCommandAndReceiveReturn(
            "config/entity_registry/update", {"entity_id": sensor_id, "area_id": area}
        )
        if not result["success"]:
            LOGGER.error(result)
            raise RuntimeError()

    def create_sensor(self, id: str, name: str, sensor_type: str, unit: str, area: str):

        uid = "".join(random.choice(string.hexdigits) for i in range(5))
        sensor_id = f"sensor.{id}"
        state_topic = f"home/{area}/{type}"

        mqtt = MqttFixture()
        mqtt.reconnect()
        sensor_mqtt = {
            "platform": "mqtt",
            "state_topic": state_topic,
            "unit_of_measurement": unit,
            "name": id,
            "friendly_name": name,
            "device_class": sensor_type,
            "uniq_id": f"{id}-{uid}",
        }

        mqtt.registerSensor(id, sensor_mqtt)
        self._assignSensorToArea(sensor_id, area)
        self.sensors[sensor_id] = state_topic

        return sensor_id

    def delete_sensor(self, sensor_id: str):
        result = runSocketCommandAndReceiveReturn(
            "config/entity_registry/remove", {"entity_id": sensor_id}
        )
        if not result["success"]:
            LOGGER.error(result)
            raise RuntimeError()
        else:
            self.sensors.pop(sensor_id)

    def update_state(self, id, value):
        mqtt = MqttFixture()
        mc = mqtt.reconnect()

        if id in self.sensors.keys():
            mc.publish(self.sensors[id], value)

    def get_state(self, id):
        result = runSocketCommandAndReceiveReturn("get_states")
        if result["success"]:
            states = result["result"]
            # LOGGER.debug(result)
            LOGGER.debug(type(states))
            if type(states) == list:
                for state in states:
                    if state["entity_id"] == id:
                        return state["state"]
            return False
        return 42


@pytest.fixture()
def SensorStubs(MQTT):
    return SensorStubClass()
