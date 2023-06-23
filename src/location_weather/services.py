from src.location_weather.models import LocationWeather


async def create_location_weather(*args, **kwargs):
    location_weather = LocationWeather(**kwargs)
    await location_weather.insert()
