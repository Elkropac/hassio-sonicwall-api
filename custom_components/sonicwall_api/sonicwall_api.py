from .const import (
    CONF_API,
    CONF_SERIAL_NUMBER,
    LOGGER
)

from .errors import AlreadyConfigured, AuthenticationRequired, CannotConnect
from custom_components.sonicwall_api.sonicwall_api_connect import SonicWallApi_Connect

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

        return True

async def get_api(
    hass, url, username_rw, password_rw, verify_ssl, login_override, login_method
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
