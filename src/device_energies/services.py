import math

from src.devices.domain import Device
from src.location_weather.domain import LocationWeather
from src.location_weather.services import calculate_sun_azimuth
from src.locations.domain import Location


def power_gen(area, eff, irrad, sysloss, cf, b, a, y):
    return area * eff * irrad * sysloss * cf * math.cos(b * math.pi / 180) * math.cos((a - y) * math.pi / 180)


async def calculate_device_energy_based_on_location_weather(
        device_type,
        location_weather: LocationWeather,
        location: Location,
        device: Device
):
    sun_azimuth = await calculate_sun_azimuth(location, location_weather.date)
    generated_power_for_one_device = power_gen(
        area=int(device_type.area),
        eff=int(device_type.system_loss),
        sysloss=int(device_type.system_loss),
        irrad=location_weather.direct_normal_irradiance,
        cf=location_weather.cloudcover,
        b=device.tilt,
        a=sun_azimuth,
        y=device.orientation
    )
    return device.count * generated_power_for_one_device
