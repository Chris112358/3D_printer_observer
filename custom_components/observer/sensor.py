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

SCAN_INTERVAL = timedelta(minutes=5)
DEFAULT_PORT = 8899
DEFAULT_IP = '192.168.178.98'

PLATFOTM_SCHEMA = PLATFORM_SCHEMA.extend(
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
    sensor = PrinterSensor(config[CONF_IP_ADDRESS], config[CONF_PORT])
    async_add_entities(sensor, update_before_add=True)
    
 



class PrinterSensor(Entity):
    def __init__(self, ip, port):
        super().__init__()

        self.addr = {'ip': ip, 'port':port}
        self.attrs: Dict[str, Any] = {}

        for key in TEMPS_LONG + STATUS + INFOS + AXIS + PROGRESS +['X_status']:
            self.attrs[key] = UNAVAILABLE

    @property
    def state(self) -> Optional[str]:
        return self.attrs[STATUS[0]]


    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        return self.attrs


    async def async_update(self):
        try:
            data = get_data(self.addr)
            self.attrs = data
        except Exception:
            _LOGGER.exception('Error during updating data for printer')

