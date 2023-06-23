import math
from datetime import datetime

from src.core.unit_of_work import AbstractUnitOfWork
from src.device_energies.domain import DeviceEnergy
from src.device_energies.exceptions import DeviceEnergyDoesNotExistsException
from src.device_types.domain import DeviceType
from src.devices.domain import Device
from src.location_weather.domain import LocationWeather


def power_gen(area, eff, irrad, sysloss, cf, b, a, y):
    return area * eff * irrad * sysloss * cf * math.cos(b * math.pi / 180) * math.cos((a - y) * math.pi / 180)


async def get_device_energy_at_date(
        date: datetime,
        device: Device,
        device_energies_uow: AbstractUnitOfWork[DeviceEnergy],
        device_type_uow: AbstractUnitOfWork[DeviceType],
        location_weather_uow: AbstractUnitOfWork[LocationWeather],
):
    device_energy_at_date = await device_energies_uow.get(device_id=device.id, date=date)
    return device_energy_at_date.value


async def calculate_device_energy_based_on_location_weather(
        device_type,
        location_weather
):
    return power_gen(
        area=int(device_type.area),
        eff=int(device_type.system_loss),
        sysloss=int(device_type.system_loss),
        irrad=location_weather.direct_normal_irradiance,
        cf=location_weather.cloudcover,
        b=10,
        a=10,
        y=10
    )