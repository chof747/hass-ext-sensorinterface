"""
Home Assistant integration to get information about next departure from specified stop in Vienna.

https://github.com/custom-components/sensorinterface/
"""

import asyncio
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import area_registry as ar
import homeassistant.helpers.config_validation as cv
from .area import get_all_areas, get_next_sensor_in_area

import voluptuous as vol
import logging

_LOGGER = logging.getLogger(__name__)


@websocket_api.websocket_command({vol.Required("type"): "sensors/areas"})
@websocket_api.async_response
async def ws_sensors_areas(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict
) -> None:
    connection.send_result(msg["id"], await get_all_areas(hass))


SENSORS_AREAS_NEXT_SCHEMA = {
    vol.Required("type"): "sensors/areas/next",
    vol.Required("area"): cv.string,
    vol.Optional("current"): cv.string,
}


@websocket_api.websocket_command(SENSORS_AREAS_NEXT_SCHEMA)
@websocket_api.async_response
async def ws_sensors_areas_next(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict
) -> None:
    if "area" in msg.keys():

        if "current" in msg.keys():
            current = msg["current"]
        else:
            current = None

        _LOGGER.info(f"Requesting next sensor in %s after %s", msg["area"], current)
        connection.send_result(
            msg["id"], await get_next_sensor_in_area(hass, msg["area"], current)
        )
    else:
        _LOGGER.warn("missing area key detected in websocket request")
        connection.send_error(
            msg["id"], "area_missing", "Missing an area to get the next sensor from"
        )


@websocket_api.websocket_command({vol.Required("type"): "sensors/list"})
@websocket_api.async_response
async def ws_sensors_list(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict
) -> None:
    """Handle listing all sensors"""
    result = []
    entReg = await er.async_get_registry(hass)
    areaReg = await ar.async_get_registry(hass)
    sensors = hass.states.async_all("sensor")

    for s in sensors:
        entity = entReg.async_get(s.entity_id)
        _LOGGER.debug(entity.area_id)
        area = areaReg.async_get_area(entity.area_id)
        if area != None:
            area_name = area.name
        else:
            area_name = "unavailable"
        value = s.state
        sensorType = entity.device_class
        result.append(
            {
                "id": s.entity_id,
                "name": entity.name,
                "area": area_name,
                "type": sensorType,
                "value": value,
            }
        )

    connection.send_result(msg["id"], result)


async def async_setup(hass, config):
    """Setup of your component."""
    hass.components.websocket_api.async_register_command(ws_sensors_list)
    hass.components.websocket_api.async_register_command(ws_sensors_areas)
    hass.components.websocket_api.async_register_command(ws_sensors_areas_next)
    return True
