"""
Adds support for the Wawin AHC 9000 thermostats
"""
import logging

from . import DOMAIN

from homeassistant.components.climate import (ClimateEntity, ClimateEntityFeature)
from homeassistant.components.climate.const import ( HVACMode, HVACAction)
from homeassistant.const import (ATTR_TEMPERATURE, UnitOfTemperature)
from .wavin_ahc9000 import WavinControl

__version__ = '0.4.0'

_LOGGER = logging.getLogger(__name__)

DEFAULT_TEMPERATURE = 22

# Values from web interface
MIN_TEMP = 10
MAX_TEMP = 35

SUPPORT_FLAGS = ClimateEntityFeature.TARGET_TEMPERATURE


def setup_platform(hass, config, add_entities, discovery_info=None):
    controller_id = discovery_info['controller_id']
    name = discovery_info['name']
    room_channel = discovery_info['room_channel']
    sensor_channel = discovery_info['sensor_channel']
    wavin_contorller = hass.data[DOMAIN][controller_id]

    add_entities([WavinThermostat(wavin_contorller, controller_id, name, room_channel, sensor_channel)])

class WavinThermostat(ClimateEntity):
    """Representation of a Wavin Thermostaat device."""

    def __init__(self, wavin_controller: WavinControl, controller_id, name, room_channel, sensor_channel):
        """Initialize the thermostat."""
        self._controller_id = controller_id
        self._sensor = wavin_controller.sensor(sensor_channel)
        self._sensor_channel = sensor_channel
        self._room = wavin_controller.room(room_channel)

        self._name = name

        self.update()

    @property
    def device_info(self):
        return {
            'name': self._name,
            'identifiers': {
                'controller': self._controller_id,
                'sensor': self._sensor_channel
            },
            'manufacturer': 'wavin'
        }

    @property
    def name(self):
        """Return the name of the thermostat."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return the unique ID for this thermostat."""
        return '_'.join(['wavin', self._controller_id,  str(self._name), 'climate'])

    @property
    def should_poll(self):
        """Polling is required."""
        return True

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return MIN_TEMP

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return MAX_TEMP

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._current_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    @property
    def hvac_mode(self):
        """Return hvac operation ie. heat, cool mode."""
        return HVACMode.HEAT

    @property
    def hvac_modes(self):
        """HVAC modes."""
        return [HVACMode.OFF, HVACMode.HEAT]

    @property
    def hvac_action(self):
        """Return the current running hvac operation."""
        if self._target_temperature < self._current_temperature:
            return HVACAction.OFF
        return HVACAction.HEATING

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        self._set_temperature(temperature)

    def _set_temperature(self, temperature, mode_int=None):

        self._room.manual_temperature = temperature

    def update(self):
        """Get the latest data."""
        self._target_temperature = self._room.desired_temperature
        self._current_temperature = self._sensor.temp_room


