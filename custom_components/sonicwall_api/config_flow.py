import voluptuous as vol

from custom_components.sonicwall_api.sonicwall_api import get_api
from .errors import AlreadyConfigured, AuthenticationRequired, CannotConnect

from homeassistant import config_entries
from homeassistant import config_entries
from homeassistant.const import (
    CONF_URL,
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_VERIFY_SSL,
)

from .const import (
    CONF_API,
    CONF_LOGIN_METHOD,
    CONF_LOGIN_METHOD_OPTIONS,
    CONF_LOGIN_OVERRIDE,
    CONF_PASSWORD_RO,
    CONF_PASSWORD_RW,
    CONF_SERIAL_NUMBER,
    CONF_USERNAME_RO,
    CONF_USERNAME_RW,
    DOMAIN,
    LOGGER
)

DEFAULT_LOGIN_METHOD = "basic"
DEFAULT_LOGIN_OVERRIDE = False
DEFAULT_VERIFY_SSL = False
DEFAULT_URL = "https://sonicwall:8443"

class SonicwallConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow."""

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            self.config = {
                CONF_URL: user_input[CONF_URL],
                CONF_USERNAME_RW: user_input[CONF_USERNAME_RW],
                CONF_PASSWORD_RW: user_input[CONF_PASSWORD_RW],
                CONF_VERIFY_SSL: user_input.get(CONF_VERIFY_SSL),
                CONF_LOGIN_METHOD: user_input.get(CONF_LOGIN_METHOD),
                CONF_LOGIN_OVERRIDE: user_input.get(CONF_LOGIN_OVERRIDE),
                CONF_SERIAL_NUMBER: None
            }
            api = await get_api(self.hass, **self.config)
            
            response = api.get('/reporting/system')
            desc = "SonicWall "+response.json()['model']+" "+response.json()[CONF_SERIAL_NUMBER]
            self.config[CONF_SERIAL_NUMBER] = response.json()[CONF_SERIAL_NUMBER]

            data = {CONF_API: self.config}
            return self.async_create_entry(title=desc, data=data)
            
            try:
                self.config = {
                    CONF_URL: user_input[CONF_URL],
                    CONF_USERNAME_RW: user_input[CONF_USERNAME_RW],
                    CONF_PASSWORD_RW: user_input[CONF_PASSWORD_RW],
                    CONF_VERIFY_SSL: user_input.get(CONF_VERIFY_SSL),
                    CONF_LOGIN_METHOD: user_input.get(CONF_LOGIN_METHOD),
                    CONF_LOGIN_OVERRIDE: user_input.get(CONF_LOGIN_OVERRIDE),
                }
                api = await get_api(self.hass, **self.config)
                
                response = api.get('/reporting/system')
                desc = "SonicWall "+response.json()['model']+" "+response.json()['serial_number']

                data = {CONF_API: self.config}

                return self.async_create_entry(title=desc, data=data)


            except AuthenticationRequired:
                errors["base"] = "faulty_credentials"

            except CannotConnect:
                errors["base"] = "service_unavailable"

            except Exception:  # pylint: disable=broad-except
                LOGGER.error(
                    "Unknown error connecting with UniFi Controller at %s",
                    user_input[CONF_URL],
                )
                return self.async_abort(reason="unknown")

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_URL, default=DEFAULT_URL): str,
                    vol.Required(CONF_USERNAME_RW): str,
                    vol.Required(CONF_PASSWORD_RW): str,
                    vol.Required(CONF_LOGIN_METHOD, default=DEFAULT_LOGIN_METHOD): vol.In(CONF_LOGIN_METHOD_OPTIONS),
                    vol.Optional(CONF_LOGIN_OVERRIDE, default=DEFAULT_LOGIN_OVERRIDE): bool,
                    vol.Optional(CONF_VERIFY_SSL, default=DEFAULT_VERIFY_SSL): bool,
                }
            ),
            errors=errors,
        )
