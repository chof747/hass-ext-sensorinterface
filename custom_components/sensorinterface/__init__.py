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

import voluptuous as vol
import logging

_LOGGER = logging.getLogger(__name__)


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
        area = areaReg.async_get_area(entity.area_id)
        value = s.state
        sensorType = entity.device_class
        result.append(
            {
                "id": s.entity_id,
                "name": entity.name,
                "area": area.name,
                "type": sensorType,
                "value": value,
            }
        )

    connection.send_result(msg["id"], result)


async def async_setup(hass, config):
    """Setup of your component."""
    _LOGGER.debug("Here! XXXX")
    hass.components.websocket_api.async_register_command(ws_sensors_list)
    return True
