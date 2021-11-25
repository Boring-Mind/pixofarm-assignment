from aiohttp import ClientSession

from common_exceptions import CommonExceptionWithResponse
from settings import Settings


class WeatherbitAPIError(CommonExceptionWithResponse):
    _default_message = "Failed to retrieve information from Weatherbit API."


class TemperatureData:
    """Represents temperature data.

    Is needed purely for typing purposes.
    """

    max_temp: float
    min_temp: float
    mean_temp: float

    def __init__(self, max_temp: float, min_temp: float, mean_temp: float):
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.mean_temp = mean_temp


class CityTemperatureRetriever:
    """Class retrieves temperature information from Weatherbit API."""

    def __init__(self, lat: float, lng: float):
        self.lat = lat
        self.lng = lng

    async def retrieve(self) -> TemperatureData:
        async with ClientSession() as http_session:
            async with http_session.get(
                Settings.WEATHER_API_ROOT,
                params={
                    "key": Settings.WEATHER_API_KEY,
                    "lat": self.lat,
                    "lon": self.lng,
                    "start_date": Settings.WEATHER_START_DATE,
                    "end_date": Settings.WEATHER_END_DATE,
                },
            ) as resp:
                if resp.status == 200:
                    temperature_data = await resp.json()

                    max_temp = temperature_data["data"]["max_temp"]
                    min_temp = temperature_data["data"]["min_temp"]
                    mean_temp = temperature_data["data"]["temp"]

                    return TemperatureData(
                        max_temp=max_temp, min_temp=min_temp, mean_temp=mean_temp
                    )
                else:
                    response = await resp.json()
                    raise WeatherbitAPIError(response=response)
