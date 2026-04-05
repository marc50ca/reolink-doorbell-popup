# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Home Assistant custom integration (`doorbell_popup`) that watches Reolink doorbell camera sensors and shows a `browser_mod` popup on all dashboards when a person or package is detected. The popup displays a live camera feed and offers two actions: open the door or dismiss.

## Integration: `custom_components/doorbell_popup`

### How it works
- Listens for `binary_sensor.front_door_person` or `binary_sensor.front_door_package` going `on`
- Calls `browser_mod.popup` with a Lovelace card containing:
  - Live feed from `camera.front_door_fluent`
  - "Open Door" button → calls `script.open_the_door`
  - "Dismiss" button → calls `browser_mod.close_popup`
- Auto-dismisses after 30 seconds (configurable)
- Debounces: same sensor won't trigger a second popup within 60 seconds

### Dependencies
- **browser_mod** must be installed via HACS — this is the mechanism for showing popups on Lovelace dashboards. Without it, a warning is logged and nothing is shown.

### Installation
Copy `custom_components/doorbell_popup/` into your HA config's `custom_components/` directory, then restart HA and add via **Settings → Devices & Services → Add Integration → Doorbell Popup**.

### Key files
| File | Purpose |
|---|---|
| `__init__.py` | State listeners, popup logic (`_show_popup`) |
| `config_flow.py` | UI setup — entity selectors for sensors, camera, script, timeout |
| `const.py` | Entity ID defaults and tunable constants (`POPUP_COOLDOWN_SECONDS`) |

### Changing behaviour
- **Cooldown between popups**: `POPUP_COOLDOWN_SECONDS` in `const.py`
- **Default entity IDs**: constants in `const.py` prefixed with `DEFAULT_`
- **Popup card layout**: `_show_popup()` in `__init__.py` — the `card` dict is a standard Lovelace card config
