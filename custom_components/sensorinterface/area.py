from array import array
import logging
from operator import attrgetter
from xml.dom.minidom import Entity
from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry, entity_registry

_LOGGER = logging.getLogger(__name__)


async def get_all_areas(hass: HomeAssistant) -> array:
    area_reg = await area_registry.async_get_registry(hass)
    result = list(map(lambda area: area.id, area_reg.async_list_areas()))
    return result


async def prepare_sensor_list(hass: HomeAssistant, area: str) -> list:
    eids = hass.states.async_entity_ids("sensor")
    ent_reg = await entity_registry.async_get_registry(hass)
    sensors = []
    selected = None

    for eid in eids:
        entity = ent_reg.async_get(eid)
        if entity.area_id == area:
            sensors.append(entity)

    if len(sensors) > 0:
        return sorted(sensors, key=attrgetter("device_class", "name"))
    else:
        return None


def build_result(hass: HomeAssistant, selected: Entity) -> dict:
    state = hass.states.get(selected.entity_id)
    return {
        "id": selected.entity_id,
        "name": selected.name,
        "type": selected.device_class,
        "value": state.state,
        "unit": selected.unit_of_measurement,
    }


async def get_next_sensor_in_area(hass: HomeAssistant, area: str, current: str) -> dict:
    sorted_sensors = await prepare_sensor_list(hass, area)

    if sorted_sensors != None:

        selected = sorted_sensors[0]
        for i in range(0, len(sorted_sensors)):
            if current == sorted_sensors[i].entity_id:
                if (i + 1) < len(sorted_sensors):
                    selected = sorted_sensors[i + 1]
                    break
                else:
                    selected = sorted_sensors[0]
                    break

        return build_result(hass, selected)
    else:
        return {}

