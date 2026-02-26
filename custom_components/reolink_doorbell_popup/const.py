"""Constants for Reolink Doorbell Popup integration."""

DOMAIN = "reolink_doorbell_popup"

CONF_CAMERA_ENTITY   = "camera_entity"
CONF_DOORBELL_SENSOR = "doorbell_sensor"
CONF_OPEN_DOOR_SCRIPT = "open_door_script"
CONF_POPUP_TIMEOUT   = "popup_timeout"

DEFAULT_CAMERA_ENTITY    = "camera.front_door_fluent"
DEFAULT_DOORBELL_SENSOR  = "binary_sensor.front_door_visitor"
DEFAULT_OPEN_DOOR_SCRIPT = "script.open_the_door"
DEFAULT_POPUP_TIMEOUT    = 30  # seconds

BLUEPRINT_SOURCE_DIR = "blueprints"
BLUEPRINT_DOMAIN_DIR = "automation"
BLUEPRINT_PACKAGE    = "reolink_doorbell_popup"
BLUEPRINT_FILENAME   = "doorbell_popup.yaml"
