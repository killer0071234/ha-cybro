"""Support for Cybro sensors."""
from __future__ import annotations

from datetime import datetime

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import STATE_CLASS_TOTAL_INCREASING
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ELECTRIC_CURRENT_MILLIAMPERE
from homeassistant.const import ELECTRIC_POTENTIAL_VOLT
from homeassistant.const import ENERGY_KILO_WATT_HOUR
from homeassistant.const import ENERGY_WATT_HOUR
from homeassistant.const import FREQUENCY_HERTZ
from homeassistant.const import PERCENTAGE
from homeassistant.const import POWER_WATT
from homeassistant.const import SPEED_KILOMETERS_PER_HOUR
from homeassistant.const import TEMP_CELSIUS
from homeassistant.const import TIME_MILLISECONDS
from homeassistant.const import TIME_MINUTES
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import AREA_ENERGY
from .const import AREA_SYSTEM
from .const import AREA_WEATHER
from .const import ATTR_DESCRIPTION
from .const import DEVICE_DESCRIPTION
from .const import DOMAIN
from .const import LOGGER
from .const import MANUFACTURER
from .const import MANUFACTURER_URL
from .coordinator import CybroDataUpdateCoordinator
from .models import CybroEntity
from cybro import VarType


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Cybro sensor based on a config entry."""
    coordinator: CybroDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    sys_tags = add_system_tags(coordinator)
    if sys_tags is not None:
        async_add_entities(sys_tags)

    temps = find_temperatures(coordinator)
    if temps is not None:
        async_add_entities(temps)

    # weather = find_weather(coordinator)
    # if weather is not None:
    #    async_add_entities(weather)

    power_meter = find_power_meter(coordinator)
    if power_meter is not None:
        async_add_entities(power_meter)


def add_system_tags(
    coordinator: CybroDataUpdateCoordinator,
) -> list[CybroSensorEntity] | None:
    """Find system tags in the plc vars.
    eg: c1000.scan_time and so on
    """
    res: list[CybroSensorEntity] = []
    var_prefix = f"c{coordinator.cybro.nad}."

    dev_info = DeviceInfo(
        identifiers={(DOMAIN, var_prefix)},
        manufacturer=MANUFACTURER,
        default_name=f"c{coordinator.cybro.nad} diagnostics",
        suggested_area=AREA_SYSTEM,
        model=DEVICE_DESCRIPTION,
        configuration_url=MANUFACTURER_URL,
    )
    # add system vars
    res.append(
        CybroSensorEntity(
            coordinator,
            f"{var_prefix}sys.ip_port",
            "",
            "",
            VarType.STR,
            EntityCategory.DIAGNOSTIC,
            None,
            1.0,
            dev_info,
        )
    )
    # find different plc diagnostic vars
    for key in coordinator.data.plc_info.plc_vars:
        if key.find(var_prefix) != -1:
            if key in (f"{var_prefix}scan_time", f"{var_prefix}scan_time_max"):
                res.append(
                    CybroSensorEntity(
                        coordinator,
                        key,
                        "",
                        TIME_MILLISECONDS,
                        VarType.INT,
                        EntityCategory.DIAGNOSTIC,
                        None,
                        1.0,
                        dev_info,
                    )
                )
            elif key in (f"{var_prefix}cybro_uptime", f"{var_prefix}operating_hours"):
                res.append(
                    CybroSensorEntity(
                        coordinator,
                        key,
                        "",
                        TIME_MINUTES,
                        VarType.INT,
                        EntityCategory.DIAGNOSTIC,
                        None,
                        1.0,
                        dev_info,
                    )
                )
            elif key in (f"{var_prefix}scan_frequency"):
                res.append(
                    CybroSensorEntity(
                        coordinator,
                        key,
                        "",
                        FREQUENCY_HERTZ,
                        VarType.INT,
                        EntityCategory.DIAGNOSTIC,
                        None,
                        1.0,
                        dev_info,
                    )
                )
            elif (
                key.find("iex_power_supply") != -1
                or key.find("cybro_power_supply") != -1
            ):
                res.append(
                    CybroSensorEntity(
                        coordinator,
                        key,
                        "",
                        ELECTRIC_POTENTIAL_VOLT,
                        VarType.INT,
                        EntityCategory.DIAGNOSTIC,
                        None,
                        0.1,
                        dev_info,
                    )
                )

    if len(res) > 0:
        return res
    return None


def find_temperatures(
    coordinator: CybroDataUpdateCoordinator,
) -> list[CybroSensorEntity] | None:
    """Find simple temperature objects in the plc vars.
    eg: c1000.th00_temperature and so on
    """
    res: list[CybroSensorEntity] = []
    dev_info = DeviceInfo(
        # entry_type=DeviceEntryType.SERVICE,
        identifiers={(DOMAIN, f"{coordinator.data.plc_info.nad}.temperatures")},
        manufacturer=MANUFACTURER,
        default_name=f"c{coordinator.data.plc_info.nad} temperatures",
        suggested_area=AREA_WEATHER,
        model=DEVICE_DESCRIPTION,
        configuration_url=MANUFACTURER_URL,
    )
    for key in coordinator.data.plc_info.plc_vars:
        if (
            key.find(".th") != -1
            or key.find(".op") != -1
            or key.find(".ts") != -1
            or key.find(".fc") != -1
        ):
            if key.find("_temperature") != -1:
                res.append(
                    CybroSensorEntity(
                        coordinator,
                        key,
                        "",
                        TEMP_CELSIUS,
                        VarType.FLOAT,
                        None,
                        SensorDeviceClass.TEMPERATURE,
                        0.1,
                        dev_info,
                    )
                )
            elif key.find("_humidity") != -1:
                res.append(
                    CybroSensorEntity(
                        coordinator,
                        key,
                        "",
                        PERCENTAGE,
                        VarType.FLOAT,
                        None,
                        SensorDeviceClass.HUMIDITY,
                        1.0,
                        dev_info,
                    )
                )

    if len(res) > 0:
        return res
    return None


def find_weather(
    coordinator: CybroDataUpdateCoordinator,
) -> list[CybroSensorEntity] | None:
    """Find simple temperature objects in the plc vars.
    eg: c1000.weather_temperature and so on
    """
    res: list[CybroSensorEntity] = []
    var_prefix = f"c{coordinator.data.plc_info.nad}.weather_"

    dev_info = DeviceInfo(
        identifiers={(DOMAIN, var_prefix)},
        manufacturer=MANUFACTURER,
        default_name=f"c{coordinator.data.plc_info.nad} weather",
        suggested_area=AREA_ENERGY,
        model=f"{DEVICE_DESCRIPTION} controller",
        configuration_url=MANUFACTURER_URL,
    )

    for key in coordinator.data.plc_info.plc_vars:
        if key.find(var_prefix) != -1:
            if key.find("_temperature") != -1:
                res.append(
                    CybroSensorEntity(
                        coordinator,
                        key,
                        "",
                        TEMP_CELSIUS,
                        VarType.FLOAT,
                        None,
                        SensorDeviceClass.TEMPERATURE,
                        0.1,
                        dev_info,
                    )
                )
            elif key.find("_humidity") != -1:
                res.append(
                    CybroSensorEntity(
                        coordinator,
                        key,
                        "",
                        PERCENTAGE,
                        VarType.FLOAT,
                        None,
                        SensorDeviceClass.HUMIDITY,
                        1.0,
                        dev_info,
                    )
                )
            elif key.find("_wind_speed") != -1:
                res.append(
                    CybroSensorEntity(
                        coordinator,
                        key,
                        "",
                        SPEED_KILOMETERS_PER_HOUR,
                        VarType.FLOAT,
                        None,
                        None,
                        0.1,
                        dev_info,
                    )
                )

    if len(res) > 0:
        return res
    return None


def find_power_meter(
    coordinator: CybroDataUpdateCoordinator,
) -> list[CybroSensorEntity] | None:
    """Find power meter objects in the plc vars.
    eg: c1000.power_meter_power and so on
    """
    res: list[CybroSensorEntity] = []
    var_prefix = f"c{coordinator.data.plc_info.nad}.power_meter"

    dev_info = DeviceInfo(
        identifiers={(DOMAIN, var_prefix)},
        manufacturer=MANUFACTURER,
        default_name=f"c{coordinator.data.plc_info.nad} power meter",
        suggested_area=AREA_ENERGY,
        model=DEVICE_DESCRIPTION,
        configuration_url=MANUFACTURER_URL,
    )
    for key in coordinator.data.plc_info.plc_vars:
        if key.find(var_prefix) != -1:
            if key.find("_power") != -1:
                res.append(
                    CybroSensorEntity(
                        coordinator,
                        key,
                        "",
                        POWER_WATT,
                        VarType.FLOAT,
                        None,
                        SensorDeviceClass.POWER,
                        1.0,
                        dev_info,
                    )
                )
            elif key.find("_voltage") != -1:
                res.append(
                    CybroSensorEntity(
                        coordinator,
                        key,
                        "",
                        ELECTRIC_POTENTIAL_VOLT,
                        VarType.FLOAT,
                        None,
                        SensorDeviceClass.VOLTAGE,
                        0.1,
                        dev_info,
                    )
                )
            elif key.find("_current") != -1:
                res.append(
                    CybroSensorEntity(
                        coordinator,
                        key,
                        "",
                        ELECTRIC_CURRENT_MILLIAMPERE,
                        VarType.FLOAT,
                        None,
                        SensorDeviceClass.CURRENT,
                        1.0,
                        dev_info,
                    )
                )
            elif key in (f"{var_prefix}_energy", f"{var_prefix}_energy_real"):
                res.append(
                    CybroSensorEntity(
                        coordinator,
                        key,
                        "",
                        ENERGY_KILO_WATT_HOUR,
                        VarType.FLOAT,
                        None,
                        SensorDeviceClass.ENERGY,
                        1.0,
                        dev_info,
                    )
                )
            elif key.find(f"{var_prefix}_energy_watthours") != -1:
                res.append(
                    CybroSensorEntity(
                        coordinator,
                        key,
                        "",
                        ENERGY_WATT_HOUR,
                        VarType.FLOAT,
                        None,
                        SensorDeviceClass.ENERGY,
                        1.0,
                        dev_info,
                    )
                )

    if len(res) > 0:
        return res
    return None


class CybroSensorEntity(CybroEntity, SensorEntity):
    """Defines a Cybro PLC sensor entity."""

    _var_type: VarType = VarType.INT
    _val_fact: float = 1.0

    def __init__(
        self,
        coordinator: CybroDataUpdateCoordinator,
        var_name: str = "",
        var_description: str = "",
        var_unit: str = "",
        var_type: VarType = VarType.INT,
        attr_entity_category: EntityCategory = None,
        attr_device_class: SensorDeviceClass = None,
        val_fact: float = 1.0,
        dev_info: DeviceInfo = None,
        # attr_icon="mdi:lightbulb",
    ) -> None:
        """Initialize a Cybro PLC sensor entity."""
        super().__init__(coordinator=coordinator)
        if var_name == "":
            return
        self._unit_of_measurement = var_unit
        self._unique_id = var_name
        self._attr_unique_id = var_name
        self._attr_name = var_description if var_description != "" else var_name
        self._state = None
        self._attr_device_info = dev_info
        self._attr_entity_category = attr_entity_category

        self._attr_device_class = attr_device_class
        if attr_device_class == SensorDeviceClass.ENERGY:
            self._attr_state_class = STATE_CLASS_TOTAL_INCREASING
        LOGGER.debug(self._attr_unique_id)
        coordinator.data.add_var(self._attr_unique_id, var_type=var_type)
        self._var_type = var_type
        self._val_fact = val_fact

    @property
    def device_info(self):
        """Return the device info."""
        if self._attr_device_info is not None:
            return self._attr_device_info
        return DeviceInfo(
            identifiers={(DOMAIN, self.platform.config_entry.unique_id)},
            manufacturer=MANUFACTURER,
            configuration_url=MANUFACTURER_URL,
            name=f"PLC {self.coordinator.cybro.nad}",
            model=f"{DEVICE_DESCRIPTION} controller",
        )

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement of the device."""
        return self._unit_of_measurement

    @property
    def native_value(self) -> datetime | StateType:
        """Return the state of the sensor."""
        res = self.coordinator.data.vars.get(self._attr_unique_id, None)
        if res is None:
            return None
        if self._var_type == VarType.INT:
            return int(int(res.value) * self._val_fact)
        if self._var_type == VarType.FLOAT:
            return float(res.value.replace(",", "")) * self._val_fact

        return res.value

    @property
    def unique_id(self):
        """Device unique id."""
        return self._unique_id

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        try:
            desc = self.coordinator.data.vars[self._attr_unique_id].description
        except KeyError:
            desc = self._attr_name
        return {
            ATTR_DESCRIPTION: desc,
        }
