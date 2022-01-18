import pytest
import requests
import os
import logging
from time import perf_counter, sleep
from pytest_socket import enable_socket, socket_allow_hosts
from .fixtures import MqttFixture


DEVICE_DISCOVERY_PATH = "./tests/stubs/setup/devices-discovery/"
LOGGER = logging.getLogger("TEST FIXTURE")
MQTT_WAIT_TIME = 12


@pytest.fixture(scope="session")
def hassendpoint():
    enable_socket()
    socket_allow_hosts(["127.0.0.1", "172.22.0.2"])

    mqtt_fixture = MqttFixture()
    mqtt_fixture.reconnect()
    if checkHomeAssIsRunningLocally():
        return True
    else:
        startTime = perf_counter()
        os.system("make test")

        while not mqtt_fixture.isHassOnline and not timeout(startTime):
            sleep(10)
        if not timeout(startTime):
            registerSensors()
            return True
        else:
            return False


def checkHomeAssIsRunningLocally():

    try:
        r = requests.get("http://localhost:8123/", timeout=5)
        return r.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def timeout(startTime: float):
    if (perf_counter() - startTime) > 120:
        LOGGER.error("Timeout starting Home Assistant")
        return True
    return False


def registerSensors():
    mqtt_fixture = MqttFixture()
    mqtt_devices = [
        f
        for f in os.listdir(DEVICE_DISCOVERY_PATH)
        if (os.path.splitext(f)[1][1:] == "json")
    ]

    for d in mqtt_devices:
        df = open(os.path.join(DEVICE_DISCOVERY_PATH, d), "r", encoding="utf-8")
        device = df.read()
        df.close()

        did = os.path.splitext(d)[0]
        mqtt_fixture.registerSensor(did, device)

    sleep(2)
