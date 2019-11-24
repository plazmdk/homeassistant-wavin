import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers import discovery

from .wavin_ahc9000 import *

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'wavin'

CONF_TTY = 'tty'
CONF_THERMOSTATS = 'thermostats'
CONF_THERMOSTAT_NAME = 'name'
CONF_THERMOSTAT_SENSOR_CHANNEL = 'sensor_channel'
CONF_THERMOSTAT_ROOM_CHANNEL = 'room_channel'

THERMOSTATS_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_THERMOSTAT_NAME): cv.string,
        vol.Required(CONF_THERMOSTAT_SENSOR_CHANNEL): cv.positive_int,
        vol.Required(CONF_THERMOSTAT_ROOM_CHANNEL): cv.positive_int
    }
)

WAVIN_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_TTY): cv.string,
        vol.Optional(CONF_THERMOSTATS, default=None): vol.Schema(vol.All(cv.ensure_list, [THERMOSTATS_SCHEMA]))
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(vol.All(cv.ensure_list, [WAVIN_SCHEMA]))
    }, extra=vol.ALLOW_EXTRA
)


def setup(hass, config):
    """Set up the WAVIN platform."""
    conf = config.get(DOMAIN)
    for index, controller_conf in enumerate(conf):
        if not wavin_setup(hass, config, controller_conf, str(index)):
            return False

    return True


def wavin_setup(hass, config, controller_conf, controller_id):
    tty = controller_conf.get(CONF_TTY)
    wavin_controller = WavinControl(tty)

    if DOMAIN not in hass.data.keys():
        hass.data[DOMAIN] = {}

    hass.data[DOMAIN][controller_id] = wavin_controller

    manual_thermostats = controller_conf.get(CONF_THERMOSTATS)
    if not manual_thermostats is None:
        _LOGGER.info("Wavin in manual setup")
        for index, thermostat_conf in enumerate(manual_thermostats):
            load_platform(hass, config, controller_id, thermostat_conf.get(CONF_THERMOSTAT_NAME),
                          thermostat_conf.get(CONF_THERMOSTAT_SENSOR_CHANNEL),
                          thermostat_conf.get(CONF_THERMOSTAT_ROOM_CHANNEL))
    else:
        _LOGGER.info("Wavin in auto setup")
        for wavin_index in wavin_controller.get_indexes():
            load_platform(hass, config, controller_id, str(wavin_index), wavin_index, wavin_index)

    return True


def load_platform(hass, config, controller_id, name, sensor_channel, room_channel):
    discovery.load_platform(hass, 'climate', DOMAIN, {
        'controller_id': controller_id,
        'name': name,
        'sensor_channel': sensor_channel,
        'room_channel': room_channel
    }, config)

    discovery.load_platform(hass, 'sensor', DOMAIN, {
        'controller_id': controller_id,
        'name': name,
        'sensor_channel': sensor_channel
    }, config)
