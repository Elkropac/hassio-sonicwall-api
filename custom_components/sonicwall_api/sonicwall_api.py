from .const import (
    CONF_API,
    CONF_SERIAL_NUMBER,
    LOGGER
)

from .errors import AlreadyConfigured, AuthenticationRequired, CannotConnect
from custom_components.sonicwall_api.sonicwall_api_connect import SonicWallApi_Connect

from homeassistant.core import callback

import hashlib
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from urllib3.exceptions import InsecureRequestWarning

#debug
#import http.client as http_client
#http_client.HTTPConnection.debuglevel = 1

class SonicWallApi:
    """Class for SonicwallAPI"""

    def __init__(self, hass, config_entry):
        """Initialize the system."""
        self.hass = hass
        self.config_entry = config_entry
        self.available = True
        self.api = None
        self.serial_number = None
        self.model = None

    async def async_setup(self):
        self.api = await get_api(
            self.hass,
            **self.config_entry.data[CONF_API]
        )
        #await self.api.login()
        response = self.api.get('/reporting/system')
        self.serial_number = response.json()[CONF_SERIAL_NUMBER]
        self.model = response.json()['model']
        self.firmware_version = response.json()['firmware_version']
        self.safemode_version = response.json()['safemode_version']
        self.rom_version = response.json()['rom_version']
        self.up_time = response.json()['up_time']
        self.last_modified_by = response.json()['last_modified_by']
        self.licenses = {}
        self.licenses['nodes_users'] = response.json()['nodes_users']
        self.licenses['ssl_vpn_nodes_users'] = response.json()['ssl_vpn_nodes_users']
        self.licenses['virtual_assist_nodes_users'] = response.json()['virtual_assist_nodes_users']
        self.licenses['vpn'] = response.json()['vpn']
        self.licenses['global_vpn_client'] = response.json()['global_vpn_client']
        self.licenses['cfs_content_filter_'] = response.json()['cfs_content_filter_']
        self.licenses['expanded_feature_set'] = response.json()['expanded_feature_set']
        self.licenses['capture_client_enforcement'] = response.json()['capture_client_enforcement']
        self.licenses['mcafee_av_enforcement'] = response.json()['mcafee_av_enforcement']
        self.licenses['client_content_filtering'] = response.json()['client_content_filtering']
        self.licenses['dpi_ssl_enforcement'] = response.json()['dpi_ssl_enforcement']
        self.licenses['gateway_anti_virus'] = response.json()['gateway_anti_virus']
        self.licenses['capture_atp'] = response.json()['capture_atp']
        self.licenses['anti_spyware'] = response.json()['anti_spyware']
        self.licenses['intrusion_prevention'] = response.json()['intrusion_prevention']
        self.licenses['app_control'] = response.json()['app_control']
        self.licenses['app_visualization'] = response.json()['app_visualization']
        self.licenses['anti_spam'] = response.json()['anti_spam']
        self.licenses['analyzer'] = response.json()['analyzer']
        self.licenses['dpi_ssl'] = response.json()['dpi_ssl']
        self.licenses['dpi_ssh'] = response.json()['dpi_ssh']
        self.licenses['wan_acceleration'] = response.json()['wan_acceleration']
        self.licenses['wxac_acceleration'] = response.json()['wxac_acceleration']
        self.licenses['botnet'] = response.json()['botnet']

        return True

    @callback
    def shutdown(self, event) -> None:
        self.api.logout()

async def get_api(
    hass, url, username_rw, password_rw, verify_ssl, login_override, login_method, serial_number
):
    url = url + '/api/sonicos'

    api = SonicWallApi_Connect(
        url,
        username=username_rw,
        password=password_rw,
        verify_ssl=verify_ssl,
        login_override=login_override,
        login_method=login_method
    )

    try:
        login = api.login()
        if (login.status_code == 401):
          LOGGER.warning("Connected to UniFi at %s but not registered.", host)
          raise AuthenticationRequired
        return api
    except requests.exceptions.RequestException:
        LOGGER.error("Error connecting to the UniFi controller at %s", host)
        raise CannotConnect
#    except aiounifi.Unauthorized:
#        LOGGER.warning("Connected to UniFi at %s but not registered.", host)
#        raise AuthenticationRequired

#    except (asyncio.TimeoutError, aiounifi.RequestError):
#        LOGGER.error("Error connecting to the UniFi controller at %s", host)
#        raise CannotConnect

#    except aiounifi.AiounifiException:
#        LOGGER.exception("Unknown UniFi communication error occurred")
#        raise AuthenticationRequired
