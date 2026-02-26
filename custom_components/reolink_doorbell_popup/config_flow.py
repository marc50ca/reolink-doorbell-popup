"""Config flow for Reolink Doorbell Popup."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_CAMERA_ENTITY,
    CONF_DOORBELL_SENSOR,
    CONF_OPEN_DOOR_SCRIPT,
    CONF_POPUP_TIMEOUT,
    DEFAULT_CAMERA_ENTITY,
    DEFAULT_DOORBELL_SENSOR,
    DEFAULT_OPEN_DOOR_SCRIPT,
    DEFAULT_POPUP_TIMEOUT,
)


def _build_schema(
    camera: str = DEFAULT_CAMERA_ENTITY,
    sensor: str = DEFAULT_DOORBELL_SENSOR,
    script: str = DEFAULT_OPEN_DOOR_SCRIPT,
    timeout: int = DEFAULT_POPUP_TIMEOUT,
) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_CAMERA_ENTITY, default=camera): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="camera")
            ),
            vol.Required(CONF_DOORBELL_SENSOR, default=sensor): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="binary_sensor")
            ),
            vol.Required(CONF_OPEN_DOOR_SCRIPT, default=script): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="script")
            ),
            vol.Required(CONF_POPUP_TIMEOUT, default=timeout): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=5,
                    max=300,
                    step=5,
                    unit_of_measurement="seconds",
                    mode=selector.NumberSelectorMode.SLIDER,
                )
            ),
        }
    )


class ReolinkDoorbellPopupConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the initial setup config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Show the setup form and create the entry on submit."""
        errors: dict[str, str] = {}

        if user_input is not None:
            hass: HomeAssistant = self.hass

            # Basic entity validation
            for key in (CONF_CAMERA_ENTITY, CONF_DOORBELL_SENSOR, CONF_OPEN_DOOR_SCRIPT):
                entity_id = user_input[key]
                if hass.states.get(entity_id) is None:
                    errors[key] = "entity_not_found"

            if not errors:
                await self.async_set_unique_id(DOMAIN)
                self._abort_if_unique_id_configured(updates=user_input)

                return self.async_create_entry(
                    title="Reolink Doorbell Popup",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=_build_schema(),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> ReolinkDoorbellPopupOptionsFlow:
        return ReolinkDoorbellPopupOptionsFlow(config_entry)


class ReolinkDoorbellPopupOptionsFlow(config_entries.OptionsFlow):
    """Allow changing settings after initial setup."""

    def __init__(self, entry: config_entries.ConfigEntry) -> None:
        self._entry = entry

    async def async_step_init(
        self, user_input: dict | None = None
    ) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self._entry.data

        return self.async_show_form(
            step_id="init",
            data_schema=_build_schema(
                camera=current.get(CONF_CAMERA_ENTITY, DEFAULT_CAMERA_ENTITY),
                sensor=current.get(CONF_DOORBELL_SENSOR, DEFAULT_DOORBELL_SENSOR),
                script=current.get(CONF_OPEN_DOOR_SCRIPT, DEFAULT_OPEN_DOOR_SCRIPT),
                timeout=int(current.get(CONF_POPUP_TIMEOUT, DEFAULT_POPUP_TIMEOUT)),
            ),
        )
