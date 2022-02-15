import pytest
import requests
import os
import logging
from time import perf_counter, sleep
from pytest_socket import enable_socket, socket_allow_hosts
from .fixtures import MQTT

DEVICE_DISCOVERY_PATH = "./tests/stubs/setup/devices-discovery/"
LOGGER = logging.getLogger("TEST FIXTURE")
MQTT_WAIT_TIME = 12


@pytest.fixture()
def sockets():
    LOGGER.info("enable sockets")
    enable_socket()
    socket_allow_hosts(["127.0.0.1", "172.22.0.2", "172.22.0.3"])


@pytest.fixture()
def hassendpoint(sockets, MQTT):

    mqtt_fixture = MQTT
    mqtt_fixture.reconnect()
    if checkHomeAssIsRunningLocally():
        return True
    else:
        startTime = perf_counter()
        os.system("make test")

        while not mqtt_fixture.isHassOnline and not timeout(startTime):
            sleep(10)
        return not timeout(startTime)


def checkHomeAssIsRunningLocally():

    try:
        r = requests.get("http://localhost:8123/", timeout=5)
        return r.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def timeout(startTime: float):
    if (perf_counter() - startTime) > 60:
        LOGGER.error("Timeout starting Home Assistant")
        return True
    return False
