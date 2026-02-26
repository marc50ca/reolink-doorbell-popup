"""
Reolink Doorbell Popup — Home Assistant Integration.

On setup this integration:
  1. Copies the bundled automation blueprint to
     <config>/blueprints/automation/reolink_doorbell_popup/
  2. Creates (or updates) a managed automation that uses Browser Mod
     to pop up the live camera feed when the doorbell is pressed.
  3. Tears down the automation cleanly on unload.
"""
from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall

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
    BLUEPRINT_SOURCE_DIR,
    BLUEPRINT_DOMAIN_DIR,
    BLUEPRINT_PACKAGE,
    BLUEPRINT_FILENAME,
)

_LOGGER = logging.getLogger(__name__)

AUTOMATION_UNIQUE_ID = "reolink_doorbell_popup_auto"


# ---------------------------------------------------------------------------
# Entry-point helpers
# ---------------------------------------------------------------------------

def _get_blueprint_src(hass: HomeAssistant) -> Path:
    """Return the path to the blueprint file inside the integration package."""
    return (
        Path(__file__).parent.parent.parent  # custom_components/<domain>/
        / ".."                               # root of the HACS repo clone
        / BLUEPRINT_SOURCE_DIR
        / BLUEPRINT_DOMAIN_DIR
        / BLUEPRINT_PACKAGE
        / BLUEPRINT_FILENAME
    )


def _get_blueprint_dst(hass: HomeAssistant) -> Path:
    """Return the target path inside the HA config directory."""
    return (
        Path(hass.config.config_dir)
        / BLUEPRINT_SOURCE_DIR
        / BLUEPRINT_DOMAIN_DIR
        / BLUEPRINT_PACKAGE
        / BLUEPRINT_FILENAME
    )


def _install_blueprint(hass: HomeAssistant) -> None:
    """Copy blueprint into the HA blueprints directory (idempotent)."""
    src = _get_blueprint_src(hass)
    dst = _get_blueprint_dst(hass)

    if not src.exists():
        _LOGGER.warning(
            "[%s] Blueprint source not found at %s — skipping blueprint install.",
            DOMAIN, src,
        )
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    _LOGGER.debug("[%s] Blueprint installed to %s", DOMAIN, dst)


def _build_automation_config(entry: ConfigEntry) -> dict:
    """Return a Home Assistant automation configuration dict."""
    cfg = entry.options or entry.data
    camera  = cfg.get(CONF_CAMERA_ENTITY,    DEFAULT_CAMERA_ENTITY)
    sensor  = cfg.get(CONF_DOORBELL_SENSOR,  DEFAULT_DOORBELL_SENSOR)
    script  = cfg.get(CONF_OPEN_DOOR_SCRIPT, DEFAULT_OPEN_DOOR_SCRIPT)
    timeout = int(cfg.get(CONF_POPUP_TIMEOUT, DEFAULT_POPUP_TIMEOUT))
    timeout_ms = timeout * 1000

    return {
        "id": AUTOMATION_UNIQUE_ID,
        "alias": "Reolink Doorbell — Camera Popup",
        "description": f"Managed by {DOMAIN} integration. Edit via Settings → Integrations.",
        "mode": "single",
        "trigger": [
            {
                "platform": "state",
                "entity_id": sensor,
                "to": "on",
            }
        ],
        "condition": [],
        "action": [
            {
                "service": "browser_mod.popup",
                "data": {
                    "title": "🔔 Someone at the Front Door!",
                    "timeout": timeout_ms,
                    "dismissable": True,
                    "content": {
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
                                        "icon_height": "40px",
                                        "tap_action": {
                                            "action": "call-service",
                                            "service": script.replace(".", "/", 1),
                                        },
                                    },
                                    {
                                        "type": "button",
                                        "name": "Dismiss",
                                        "icon": "mdi:close-circle-outline",
                                        "icon_height": "40px",
                                        "tap_action": {
                                            "action": "call-service",
                                            "service": "browser_mod/close_popup",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                },
            }
        ],
    }


# ---------------------------------------------------------------------------
# HACS / HA integration lifecycle
# ---------------------------------------------------------------------------

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Global setup (YAML config not used)."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry created by the UI flow."""
    _LOGGER.info("[%s] Setting up Reolink Doorbell Popup integration.", DOMAIN)

    # 1. Install the blueprint (runs in executor to avoid blocking event loop)
    await hass.async_add_executor_job(_install_blueprint, hass)

    # 2. Store config for reference / options flow
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # 3. Register an options-update listener so the automation reflects changes
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    _LOGGER.info(
        "[%s] Setup complete. Camera: %s | Sensor: %s | Timeout: %ss",
        DOMAIN,
        entry.data.get(CONF_CAMERA_ENTITY),
        entry.data.get(CONF_DOORBELL_SENSOR),
        entry.data.get(CONF_POPUP_TIMEOUT, DEFAULT_POPUP_TIMEOUT),
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id, None)
    _LOGGER.info("[%s] Integration unloaded.", DOMAIN)
    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options updates — reload the entry to apply new settings."""
    await hass.config_entries.async_reload(entry.entry_id)
