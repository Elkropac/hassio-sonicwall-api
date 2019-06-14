""" SonicWALL api device tracker """

import logging
import voluptuous as vol
import time

import homeassistant.helpers.config_validation as cv
from homeassistant.components.device_tracker import (
    DOMAIN, PLATFORM_SCHEMA, DeviceScanner)
from homeassistant.const import (
    CONF_URL, CONF_VERIFY_SSL)

from custom_components.sonicwall_api.sonicwall_api import SonicWallApi
from custom_components.sonicwall_api.const import (
    CONF_USERNAME_RO, CONF_USERNAME_RW, CONF_PASSWORD_RO, CONF_PASSWORD_RW, CONF_DEVICE_TRACKER_INTERFACES)

_LOGGER = logging.getLogger(__name__)

_LOGGER.info("Checking SonicWALL API")

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_URL): cv.string,
    vol.Required(CONF_PASSWORD_RO): cv.string,
    vol.Required(CONF_USERNAME_RO): cv.string,
    vol.Optional(CONF_PASSWORD_RW): cv.string,
    vol.Optional(CONF_USERNAME_RW): cv.string,
    vol.Optional(CONF_DEVICE_TRACKER_INTERFACES, default=['X0']): vol.Schema([str]),
    vol.Optional(CONF_VERIFY_SSL, default=False): cv.boolean,
})

def get_scanner(hass, config):
    """Validate the configuration and return a SonicwallApi."""
    _LOGGER.debug("SonicWALL login")
    return SonicwallDeviceScanner(config[DOMAIN])

class SonicwallDeviceScanner(DeviceScanner):
    def __init__(self, config):
        """Initialize the scanner."""
        self.url = config[CONF_URL]
        self.username_ro = config[CONF_USERNAME_RO]
        self.password_ro = config[CONF_PASSWORD_RO]
        self.verify_ssl = config[CONF_VERIFY_SSL]
        self.filter_interfaces = config[CONF_DEVICE_TRACKER_INTERFACES]

        self.last_results = []

        self.scanner = SonicWallApi(self.url, self.username_ro, self.password_ro, self.verify_ssl)

        # Check if the access point is accessible
        response = self.scanner.login()
        success = response['status']['success']
        self.system_info = self.scanner.get('/reporting/system')
        response = self.scanner.logout()
        if not success:
            raise ConnectionError("Cannot connect to Sonicwall failed")

        status_string = "SonicWALL API; Connected to model '{model}'; serial number: '{serial_number}', firmware version: '{firmware_version}'".format(**self.system_info)
        print(status_string)
        _LOGGER.info(status_string)

    def scan_devices(self):
        """Scan for new devices and return a list with found device IDs."""
        self._update_info()

        return self.last_results

    def get_device_name(self, device):
        """waiting for dhcp leases api return hostname"""
        return None

    def _update_info(self):
        """Check for connected devices."""

        self.last_results = []
        response = self._make_request()
        #print(response)
        #_LOGGER.info(response)
        for client in response:
            if 'type' not in client or 'interface' not in client or 'mac_address' not in client:
                print(client)
                continue
            """use only dynamic ARP entries"""
            if client['type'] != 'Dynamic':
                continue
            """filter out unwanted interfaces"""
            if 'all' not in self.filter_interfaces and client['interface'] not in self.filter_interfaces:
                continue
            self.last_results.append(client['mac_address']+'-'+client['interface'])

        return True

    def _make_request(self):
        _LOGGER.info("Sonicwall API checking arp table")
        self.scanner.login()
        response = self.scanner.get('/reporting/arp/cache')
        self.scanner.logout()

        return response
