"""Config flow for Doorbell Popup."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_PERSON_SENSOR,
    CONF_PACKAGE_SENSOR,
    CONF_CAMERA,
    CONF_DOOR_SCRIPT,
    CONF_TIMEOUT,
    DEFAULT_TIMEOUT,
    DEFAULT_PERSON_SENSOR,
    DEFAULT_PACKAGE_SENSOR,
    DEFAULT_CAMERA,
    DEFAULT_DOOR_SCRIPT,
)

STEP_USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PERSON_SENSOR, default=DEFAULT_PERSON_SENSOR): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="binary_sensor")
        ),
        vol.Required(CONF_PACKAGE_SENSOR, default=DEFAULT_PACKAGE_SENSOR): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="binary_sensor")
        ),
        vol.Required(CONF_CAMERA, default=DEFAULT_CAMERA): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="camera")
        ),
        vol.Required(CONF_DOOR_SCRIPT, default=DEFAULT_DOOR_SCRIPT): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="script")
        ),
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): selector.NumberSelector(
            selector.NumberSelectorConfig(min=5, max=300, step=5, unit_of_measurement="seconds", mode="slider")
        ),
    }
)


class DoorbellPopupConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> config_entries.FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            for key in (CONF_PERSON_SENSOR, CONF_PACKAGE_SENSOR, CONF_CAMERA):
                if self.hass.states.get(user_input[key]) is None:
                    errors[key] = "entity_not_found"

            if not errors:
                await self.async_set_unique_id(DOMAIN)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="Doorbell Popup", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_SCHEMA,
            errors=errors,
        )
