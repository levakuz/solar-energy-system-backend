import datetime

import httpx

from src.location_weather.domain import LocationWeather
from src.location_weather.services import create_location_weather


async def get_weather_for_last_day(
        latitude: float,
        longitude: float,
        location_id: int
):
    end_date = datetime.datetime.today().date()
    start_date = end_date - datetime.timedelta(days=1)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'https://api.open-meteo.com/v1/forecast?'
            + f'latitude={latitude}&longitude={longitude}'
            + '&hourly=cloudcover,direct_normal_irradiance'
            + '&past_days=1&forecast_days=0'
        )
    for index, time_moment in enumerate(response.json()["hourly"]["time"]):
        await create_location_weather(
            **LocationWeather(
                location_id=location_id,
                date=time_moment,
                direct_normal_irradiance=response.json()["hourly"]["direct_normal_irradiance"][index],
                cloudcover=response.json()["hourly"]["cloudcover"][index]
            ).dict()
        )
