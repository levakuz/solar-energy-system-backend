from datetime import datetime

import httpx
import suncalc

from src.location_weather.models import LocationWeather
from src.locations.domain import Location


async def create_location_weather(*args, **kwargs):
    location_weather = LocationWeather(**kwargs)
    await location_weather.insert()


async def get_weather_for_date(
        date_from: datetime,
        date_to: datetime,
        latitude: float,
        longitude: float,
        location_id: int
) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'https://api.open-meteo.com/v1/forecast?'
            + f'latitude={latitude}&longitude={longitude}'
            + '&hourly=cloudcover,direct_normal_irradiance'
            + f'&start_date={date_from.date().isoformat()}&end_date={date_to.date().isoformat()}'
        )
    return await parse_weather_from_api(response.json(), location_id)


async def parse_weather_from_api(response: dict, location_id: int) -> dict:
    result = {}
    for index, time_moment in enumerate(response["hourly"]["time"]):
        if not response["hourly"]["direct_normal_irradiance"][index]:
            response["hourly"]["direct_normal_irradiance"][index] = 0
        if not response["hourly"]["cloudcover"][index]:
            response["hourly"]["cloudcover"][index] = 0
        lw = LocationWeather(
            location_id=location_id,
            date=time_moment,
            direct_normal_irradiance=response["hourly"]["direct_normal_irradiance"][index],
            cloudcover=response["hourly"]["cloudcover"][index]
        )
        await create_location_weather(
            **lw.dict()
        )
        result[datetime.fromisoformat(time_moment).isoformat()] = lw
    return result


async def calculate_sun_azimuth(location: Location, date: datetime) -> float:
    position = suncalc.get_position(date, lng=location.longitude, lat=location.latitude)
    return position["azimuth"]
