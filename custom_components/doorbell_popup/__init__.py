"""Doorbell Popup integration — shows a browser_mod popup with camera feed
and action buttons when a person or package is detected at the front door."""
import logging
from datetime import datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback, Event
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    DOMAIN,
    CONF_PERSON_SENSOR,
    CONF_PACKAGE_SENSOR,
    CONF_CAMERA,
    CONF_DOOR_SCRIPT,
    CONF_TIMEOUT,
    DEFAULT_TIMEOUT,
    POPUP_COOLDOWN_SECONDS,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    person_sensor: str = entry.data[CONF_PERSON_SENSOR]
    package_sensor: str = entry.data[CONF_PACKAGE_SENSOR]
    camera: str = entry.data[CONF_CAMERA]
    door_script: str = entry.data[CONF_DOOR_SCRIPT]
    timeout: int = entry.data.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)

    last_popup: dict[str, datetime] = {}

    @callback
    def _on_sensor_triggered(event: Event) -> None:
        new_state = event.data.get("new_state")
        if new_state is None or new_state.state != "on":
            return

        entity_id: str = event.data["entity_id"]
        now = datetime.now()

        last = last_popup.get(entity_id)
        if last and (now - last).total_seconds() < POPUP_COOLDOWN_SECONDS:
            return

        last_popup[entity_id] = now

        title = (
            "Person Detected at Front Door"
            if entity_id == person_sensor
            else "Package Detected at Front Door"
        )

        hass.async_create_task(
            _show_popup(hass, title, camera, door_script, timeout)
        )

    unsub = async_track_state_change_event(
        hass,
        [person_sensor, package_sensor],
        _on_sensor_triggered,
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {"unsub": unsub}

    return True


async def _show_popup(
    hass: HomeAssistant,
    title: str,
    camera: str,
    door_script: str,
    timeout: int,
) -> None:
    if not hass.services.has_service("browser_mod", "popup"):
        _LOGGER.warning(
            "browser_mod is not installed. Install HACS and browser_mod to enable "
            "doorbell popups. See https://github.com/thomasloven/hass-browser_mod"
        )
        return

    card = {
        "type": "vertical-stack",
        "cards": [
            {
                "type": "picture-entity",
                "entity": camera,
                "camera_view": "live",
                "show_name": False,
                "show_state": False,
            },
            {
                "type": "horizontal-stack",
                "cards": [
                    {
                        "type": "button",
                        "name": "Open Door",
                        "icon": "mdi:door-open",
                        "tap_action": {
                            "action": "call-service",
                            "service": door_script.replace(".", "/", 1),
                        },
                    },
                    {
                        "type": "button",
                        "name": "Dismiss",
                        "icon": "mdi:close",
                        "tap_action": {
                            "action": "call-service",
                            "service": "browser_mod/close_popup",
                        },
                    },
                ],
            },
        ],
    }

    await hass.services.async_call(
        "browser_mod",
        "popup",
        {
            "title": title,
            "card": card,
            "timeout": timeout * 1000,
            "dismissable": True,
        },
    )


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = hass.data[DOMAIN].pop(entry.entry_id, {})
    unsub = data.get("unsub")
    if unsub:
        unsub()
    return True
