"""The sonicwall_api component."""
#import voluptuous as vol

from homeassistant.core import callback
#from homeassistant.const import (
#    CONF_URL, CONF_VERIFY_SSL)

from .const import DOMAIN

async def async_setup(hass, config):
    hass.states.async_set("sonicwall_api.world", "Paulus")

    # Return boolean to indicate that initialization was successful.
    return True

async def async_setup_entry(hass, config_entry):
    """Set up the UniFi component."""
    hass.data.setdefault(UNIFI_DOMAIN, {})

    controller = UniFiController(hass, config_entry)
    if not await controller.async_setup():
        return False

    hass.data[UNIFI_DOMAIN][config_entry.entry_id] = controller

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, controller.shutdown)

    LOGGER.debug("UniFi config options %s", config_entry.options)

    if controller.mac is None:
        return True

    device_registry = await hass.helpers.device_registry.async_get_registry()
    device_registry.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        connections={(CONNECTION_NETWORK_MAC, controller.mac)},
        manufacturer=ATTR_MANUFACTURER,
        model="UniFi Controller",
        name="UniFi Controller",
        # sw_version=config.raw['swversion'],
    )

    return True
