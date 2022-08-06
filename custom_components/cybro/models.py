"""Models for Cybro."""
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import (
    ATTR_SW_VERSION,
    ATTR_MODEL,
    ATTR_CONFIGURATION_URL,
    ATTR_MANUFACTURER,
    ATTR_NAME,
    ATTR_IDENTIFIERS,
)
from .const import DEVICE_DESCRIPTION, MANUFACTURER, MANUFACTURER_URL
from .coordinator import CybroDataUpdateCoordinator


class CybroEntity(CoordinatorEntity):
    """Defines a base Cybro entity."""

    coordinator: CybroDataUpdateCoordinator

    @property
    def device_info(self):
        """Return device information about this Cybro device."""
        return {
            ATTR_IDENTIFIERS: {
                # Serial numbers are unique identifiers within a specific domain
                (self.coordinator.cybro.nad, self.name)
            },
            ATTR_NAME: self.name,
            ATTR_MANUFACTURER: MANUFACTURER,
            ATTR_MODEL: DEVICE_DESCRIPTION,
            ATTR_SW_VERSION: self.coordinator.data.server_info.server_version,
            ATTR_CONFIGURATION_URL: MANUFACTURER_URL,
        }
