""" MQTT Fixture singelton class"""

import logging
import pytest

from time import sleep
from paho.mqtt import client as mqtt

LOGGER = logging.getLogger("MQTT Fixture")

HASS_STATUS_TOPIC = "homeassistant/status"


class MqttFixture(object):
    _instance = None
    _mqttClient = None
    _hassStatus = None

    def __new__(cls):
        if cls._instance == None:
            cls._instance = super(MqttFixture, cls).__new__(cls)
            cls._instance._startUp()
        return cls._instance

    def on_connect(self, _client, _userdata, _flags, rc):
        if rc == 0:
            LOGGER.debug("connected to MQTT Host")
        else:
            LOGGER.error(f"Bad connection Returned code={rc}")

    def on_message(self, _client, _userdata, message: mqtt.MQTTMessage):
        if message.topic == HASS_STATUS_TOPIC:
            self._hassStatus = message.payload.decode("utf-8")

    def _startUp(self):
        self._mqttClient = mqtt.Client("sensif_test")
        self._mqttClient.on_connect = self.on_connect
        self._mqttClient.on_message = self.on_message

    def reconnect(self):
        if not self._mqttClient.is_connected():
            self._mqttClient.connect("mqtt")
            self._mqttClient.subscribe(HASS_STATUS_TOPIC)
            self._mqttClient.loop_start()
            while not self._mqttClient.is_connected():
                sleep(1)
        return self._mqttClient

    @property
    def hassStatus(self):
        return self._hassStatus

    @property
    def isHassOnline(self):
        return self._hassStatus == "online"

    def registerSensor(self, did, device):
        self._mqttClient.reconnect()
        self._mqttClient.publish(f"homeassistant/sensor/{did}/config", device)


@pytest.fixture(scope="session")
def MQTT():
    return MqttFixture()
