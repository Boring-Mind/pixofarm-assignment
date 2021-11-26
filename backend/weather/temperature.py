from datetime import datetime
from typing import List, Any, Dict

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
    date: datetime

    def __init__(
        self, max_temp: float, min_temp: float, mean_temp: float, date: datetime
    ):
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.mean_temp = mean_temp
        self.date = date

    def to_db_dict(self) -> Dict[str, Any]:
        """Convert entry to be inserted into DB as a Temperature model instance."""
        return {
            "max": self.max_temp,
            "min": self.min_temp,
            "mean": self.mean_temp,
            "date": self.date,
        }


class CityTemperatureRetriever:
    """Class retrieves temperature information from Weatherbit API."""

    def __init__(self, lat: float, lng: float):
        self.lat = lat
        self.lng = lng

    @classmethod
    def parse_retrieved_data(cls, data: Dict[str, Any]) -> List[TemperatureData]:
        data = data["data"]
        parsed_list: list[TemperatureData] = []

        for entry in data:
            parsed_list.append(
                TemperatureData(
                    max_temp=entry["max_temp"],
                    min_temp=entry["min_temp"],
                    mean_temp=entry["temp"],
                    date=datetime.fromtimestamp(entry["ts"]),
                )
            )
        return parsed_list

    async def retrieve(self) -> List[TemperatureData]:
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

                    return self.parse_retrieved_data(temperature_data)
                else:
                    response = await resp.json()
                    raise WeatherbitAPIError(response=response)
