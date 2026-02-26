# 🔔 Reolink Doorbell Popup

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2023.6%2B-blue.svg)](https://www.home-assistant.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Pop up a **live camera feed** on every registered browser/device the moment your
Reolink doorbell is pressed — with a one-tap **Open Door** button and a
configurable **auto-dismiss timer** (default 30 seconds).

![Popup preview](.github/preview.png)

---

## Features

- 📹 Live camera stream appears instantly on all registered browsers / phones
- 🚪 One-tap **Open Door** button calls your unlock script
- ⏱️ Configurable auto-dismiss timeout (5 – 300 s, default **30 s**)
- ⚙️ Fully configured via the HA UI — no YAML editing required
- 📋 Ships with a reusable **Automation Blueprint** for advanced customisation
- 🗺️ Optional Lovelace dashboard card for always-visible monitoring

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Home Assistant 2023.6+ | Config-flow integrations with entity selectors |
| [Browser Mod](https://github.com/thomasloven/hass-browser_mod) | Enables popup windows in your browsers. Install via HACS. |
| Reolink camera integrated into HA | Entity type: `camera`, camera_view `live` |

---

## Installation via HACS

### Option A — One-click (once this repo is in the HACS default store)

1. Open **HACS → Integrations**
2. Search for **Reolink Doorbell Popup** and click **Download**
3. Restart Home Assistant

### Option B — Custom Repository

1. Open **HACS → Integrations → ⋮ → Custom repositories**
2. Enter: `https://github.com/marc50/reolink-doorbell-popup`
3. Category: **Integration**
4. Click **Add**, then find and install **Reolink Doorbell Popup**
5. Restart Home Assistant

---

## Setup

After restarting HA:

1. Go to **Settings → Devices & Services → + Add Integration**
2. Search for **Reolink Doorbell Popup**
3. Fill in the configuration form:

| Field | Description | Default |
|---|---|---|
| Camera entity | Your live camera feed | `camera.front_door_fluent` |
| Doorbell binary sensor | Triggers the popup | `binary_sensor.front_door_visitor` |
| Open-door script | Runs when "Open Door" is tapped | `script.open_the_door` |
| Auto-dismiss timeout | Seconds before popup closes | `30` |

4. Click **Submit** — that's it! 🎉

### Changing settings later

Go to **Settings → Devices & Services → Reolink Doorbell Popup → Configure**
and update any value. Changes take effect immediately.

---

## How it works

```
Visitor presses doorbell
         │
         ▼
binary_sensor.front_door_visitor → ON
         │
         ▼
  Automation triggers
  browser_mod.popup fires
         │
         ▼
┌────────────────────────────────┐
│  🔔 Someone at the Front Door! │
│  ┌──────────────────────────┐  │
│  │    LIVE CAMERA FEED      │  │
│  │  camera.front_door_..    │  │
│  └──────────────────────────┘  │
│  [ Open Door ]   [ Dismiss ]   │
│                                │
│  Auto-closes in 30 s ──────── │
└────────────────────────────────┘
         │
         ▼ (if Open Door tapped)
  script.open_the_door runs
```

---

## Using the Blueprint directly

The integration ships with a standalone blueprint if you prefer to manage
the automation yourself:

1. After installing via HACS, the blueprint is automatically available at
   **Settings → Automations & Scenes → Blueprints**
2. Find **"Reolink Doorbell — Camera Popup"** and click **Create Automation**
3. Fill in the inputs and save

Alternatively, import it manually:

**Settings → Automations → Blueprints → Import Blueprint**

```
https://github.com/YOUR_USERNAME/reolink-doorbell-popup/raw/main/blueprints/automation/reolink_doorbell_popup/doorbell_popup.yaml
```

---

## Lovelace Dashboard Card

Add the optional always-visible monitor card to any dashboard:

1. Edit your dashboard → **+ Add Card → Manual Card**
2. Paste the contents of
   [`lovelace/doorbell-monitor-card.yaml`](lovelace/doorbell-monitor-card.yaml)
3. Save

The card shows the live feed, visitor status, Open Door / Full Screen buttons,
and a 24-hour activity graph.

---

## Targeting specific devices

By default, the popup appears on **all** registered Browser Mod browsers.
To restrict it to specific devices:

1. Open Browser Mod settings and note the **browser ID** for each device
2. Edit the managed automation
   (**Settings → Automations → "Reolink Doorbell — Camera Popup"**)
3. Add a `browser_id` list to the `browser_mod.popup` service call:

```yaml
service: browser_mod.popup
data:
  browser_id:
    - my_phone_abc123
    - kitchen_tablet_xyz
  ...
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Popup never appears | Confirm Browser Mod is installed and your browser is registered (Settings → Browser Mod → Registered Browsers) |
| Camera shows a still image | Ensure your camera integration supports HA streaming; check `camera_view: live` is set |
| "entity_not_found" error on setup | Verify the entity IDs exist and HA has loaded them before running setup |
| Popup appears but "Open Door" fails | Check `script.open_the_door` exists under Settings → Automations & Scenes → Scripts |
| Want different timeout | Go to Settings → Integrations → Reolink Doorbell Popup → Configure |

---

## Repository structure

```
reolink-doorbell-popup/
├── hacs.json                                  # HACS metadata
├── README.md
├── LICENSE
├── custom_components/
│   └── reolink_doorbell_popup/
│       ├── __init__.py                        # Integration setup & blueprint installer
│       ├── manifest.json                      # HA integration manifest
│       ├── config_flow.py                     # UI config & options flow
│       ├── const.py                           # Constants
│       ├── strings.json                       # UI labels
│       └── translations/
│           └── en.json
├── blueprints/
│   └── automation/
│       └── reolink_doorbell_popup/
│           └── doorbell_popup.yaml            # Parameterised automation blueprint
└── lovelace/
    └── doorbell-monitor-card.yaml             # Optional dashboard card
```

---

## License

MIT — see [LICENSE](LICENSE) for details.
