import logging
from datetime import timedelta

from typing import Any, Callable, Dict, Optional

from .recieve_data import get_data
from .const import TEMPS_LONG, INFOS, STATUS, AXIS, PROGRESS
from .const import UNAVAILABLE

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_IP_ADDRESS, CONF_PORT
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)


_LOGGER = logging.getLogger(__name__)

#SCAN_INTERVAL = timedelta(minutes=5)
DEFAULT_PORT = 8899
DEFAULT_IP = '192.168.178.98'
TOTAL_KEYS = TEMPS_LONG + STATUS + INFOS + AXIS + PROGRESS +['X_status']


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
                        {
                            vol.Optional(CONF_IP_ADDRESS, default=DEFAULT_IP): cv.string,
                            vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
                            })


async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """Set up the sensor platform."""

    ip = config[CONF_IP_ADDRESS]
    port =  config[CONF_PORT]

    sensors = [ PrinterSensor(ip, port, key) for key in TOTAL_KEYS ]

    async_add_entities(sensors, update_before_add=True)
    
 



class PrinterSensor(Entity):
    def __init__(self, ip, port, name):
        super().__init__()

        self.addr = {'ip': ip, 'port':port}
        self.attrs: Dict[str, Any] = {}
        self._name = name
        self._available = True

        for key in TOTAL_KEYS:
            self.attrs[key] = UNAVAILABLE

    @property
    def state(self) -> Optional[str]:
        return self.attrs[self._name]

    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        _LOGGER.debug(self.attrs)
        return self.attrs

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self.attrs


    @property
    def name(self):
        return '3D_print_' + self._name

    @property
    def available(self):
        return self._available

    @property
    def unique_id(self) -> str:
        return self.attrs[INFOS[3]] + self._name


    async def async_update(self):
        try:
            data = get_data(self.addr)
            self.attrs = data
            _LOGGER.debug('Updated data for printer')
        except Exception:
            _LOGGER.exception('Error during updating data for printer')

