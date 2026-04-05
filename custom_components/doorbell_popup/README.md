# Doorbell Popup

A Home Assistant custom integration that watches a Reolink doorbell camera and shows a `browser_mod` popup on all dashboards when a person or package is detected. The popup displays a live camera feed with buttons to open the door or dismiss.

## Prerequisites

- **HACS** installed in Home Assistant
- **browser_mod** installed via HACS ([thomasloven/hass-browser_mod](https://github.com/thomasloven/hass-browser_mod))
- A Reolink doorbell camera integrated into HA with:
  - A person detection binary sensor (default: `binary_sensor.front_door_person`)
  - A package detection binary sensor (default: `binary_sensor.front_door_package`)
  - A camera entity with live streaming (default: `camera.front_door_fluent`)
- A script to unlock the door (default: `script.open_the_door`)

## Installation

1. Copy the `custom_components/doorbell_popup/` directory into your HA config folder:

   ```
   <config>/
   └── custom_components/
       └── doorbell_popup/
           ├── __init__.py
           ├── config_flow.py
           ├── const.py
           ├── manifest.json
           ├── strings.json
           └── translations/
               └── en.json
   ```

2. Restart Home Assistant.

3. Go to **Settings → Devices & Services → Add Integration** and search for **Doorbell Popup**.

4. Complete the setup — enter the entity IDs for your sensors, camera, door script, and auto-dismiss timeout (default: 30 seconds).

## How It Works

When the person or package sensor turns `on`, a popup appears on all active Lovelace dashboards showing:

- A live camera feed
- An **Open Door** button (calls your door script)
- A **Dismiss** button

The popup auto-dismisses after the configured timeout. The same sensor won't re-trigger a popup within 60 seconds.

## Customisation

| What | Where |
|---|---|
| Cooldown between popups | `POPUP_COOLDOWN_SECONDS` in `const.py` |
| Default entity IDs | `DEFAULT_*` constants in `const.py` |
| Popup card layout | `_show_popup()` in `__init__.py` |
