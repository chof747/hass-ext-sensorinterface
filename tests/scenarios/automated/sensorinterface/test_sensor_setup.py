import logging
import pytest
from .fixtures.sensor_stub import SensorStubs

LOGGER = logging.getLogger("WEBSOCKET_AREA")


def test_sensor_stub(sockets, hassendpoint, SensorStubs):
    sensor_id = SensorStubs.create_sensor(
        "wslr_temp", "Temperature Living Room", "temperature", "°C", "wohnzimmer"
    )
    SensorStubs.update_state(sensor_id, 23.4)
    assert pytest.approx(
        float(SensorStubs.get_state(sensor_id)), 0.01
    ) == pytest.approx(23.4, 0.01)
    # SensorStubs.delete_sensor(sensor_id)

