from time import sleep
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

    def _finalizeSensorToArea(
        self, sensor_id: str, area: str, friendly_name: str, device_class: str
    ):

        result = runSocketCommandAndReceiveReturn(
            "config/entity_registry/update",
            {
                "entity_id": sensor_id,
                "area_id": area,
                "name": friendly_name,
                "device_class": device_class,
            },
        )

        if not result["success"]:
            LOGGER.error(result)
            raise RuntimeError()

    def create_sensor(self, id: str, name: str, sensor_type: str, unit: str, area: str):

        uid = "".join(random.choice(string.hexdigits) for i in range(5))
        sensor_id = f"sensor.{id}"
        state_topic = f"home/{area}/{type}/{id}"

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

        while self.get_state(sensor_id) == False:
            mqtt.registerSensor(id, sensor_mqtt)
        self._finalizeSensorToArea(sensor_id, area, name, sensor_type)
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

    def delete_all(self):
        while len(self.sensors.keys()) > 0:
            self.delete_sensor(next(iter(self.sensors)))

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
        return False


@pytest.fixture()
def SensorStubs(MQTT):
    sensorstub = SensorStubClass()
    yield sensorstub
    sensorstub.delete_all()
