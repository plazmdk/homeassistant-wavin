from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor.const import SensorDeviceClass

from . import DOMAIN
from .wavin_ahc9000 import WavinControl


def setup_platform(hass, config, add_entities, discovery_info=None):
    controller_id = discovery_info['controller_id']
    name = discovery_info['name']
    sensor_channel = discovery_info['sensor_channel']
    wavin_contorller = hass.data[DOMAIN][controller_id]
    add_entities([WavinSensor(wavin_contorller, controller_id, name, sensor_channel)])


class WavinSensor(Entity):
    """Implementation of the IHC sensor."""

    def __init__(self, wavin_controller: WavinControl, controller_id, name, sensor_channel):
        """Initialize the thermostat."""

        self._controller_id = controller_id
        self._sensor = wavin_controller.sensor(sensor_channel)
        self._sensor_channel = sensor_channel
        self._name = name

    @property
    def device_class(self):
        return SensorDeviceClass.BATTERY

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
    def should_poll(self) -> bool:
        return True

    @property
    def name(self):
        """Return the device name."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return the unique ID for this thermostat battery."""
        return '_'.join(['wavin', self._controller_id,  str(self._name), 'battery'])

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._battery

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return '%'

    def update(self):
        self._battery = self._sensor.battery
