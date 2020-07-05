"""Errors for the UniFi component."""
from homeassistant.exceptions import HomeAssistantError


class SonicWallApiException(HomeAssistantError):
    """Base class for UniFi exceptions."""


class AlreadyConfigured(SonicWallApiException):
    """Controller is already configured."""


class AuthenticationRequired(SonicWallApiException):
    """Unknown error occurred."""


class CannotConnect(SonicWallApiException):
    """Unable to connect to the controller."""


class LoginRequired(SonicWallApiException):
    """Component got logged out."""


class UserLevel(SonicWallApiException):
    """User level too low."""
