"""The sonicwall_api component."""


from .const import (
    ATTR_MANUFACTURER,
    CONF_API,
    DOMAIN,
    LOGGER,
)
from custom_components.sonicwall_api.sonicwall_api import SonicWallApi

from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC

async def async_setup(hass, config):
    hass.states.async_set("sonicwall_api.world", "Paulus")

    # Return boolean to indicate that initialization was successful.
    return True

async def async_setup_entry(hass, config_entry):
    """Set up the UniFi component."""
    hass.data.setdefault(DOMAIN, {})

    api = SonicWallApi(hass, config_entry)
    if not await api.async_setup():
        return False

    hass.data[DOMAIN][config_entry.entry_id] = api

    #hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, controller.shutdown)

    LOGGER.debug("SonicWallApi config options %s", config_entry.options)

    device_registry = await hass.helpers.device_registry.async_get_registry()
    device_registry.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        connections={(CONNECTION_NETWORK_MAC, api.serial_number)},
        manufacturer=ATTR_MANUFACTURER,
        model=api.model,
        name=ATTR_MANUFACTURER+" "+api.model+" "+api.serial_number,
        # sw_version=config.raw['swversion'],
    )

    return True
