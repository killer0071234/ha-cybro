"""DataUpdateCoordinator for Cybro PLC."""
from __future__ import annotations

from collections.abc import Callable

from cybro import Cybro, CybroError, Device as CybroDevice

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS, CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, SCAN_INTERVAL


class CybroDataUpdateCoordinator(DataUpdateCoordinator[CybroDevice]):
    """Class to manage fetching Cybro PLC data from scgi server."""

    config_entry: ConfigEntry
    unique_id: str

    def __init__(
        self,
        hass: HomeAssistant,
        *,
        entry: ConfigEntry,
    ) -> None:
        """Initialize global Cybro data updater."""
        self.cybro = Cybro(
            entry.data[CONF_HOST],
            entry.data[CONF_PORT],
            entry.data[CONF_ADDRESS],
            session=async_get_clientsession(hass),
        )
        self.unique_id = "c" + str(entry.data[CONF_ADDRESS])
        self.unsub: Callable | None = None

        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> CybroDevice:
        """Fetch data from Cybro."""
        try:
            device = await self.cybro.update(full_update=not self.last_update_success)
        except CybroError as error:
            raise UpdateFailed(
                f"Invalid response from Cybro scgi server: {error}"
            ) from error

        self.async_update_listeners()

        return device
