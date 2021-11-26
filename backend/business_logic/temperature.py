from typing import List

import pandas as pd
from remote_pdb import RemotePdb
from sqlalchemy.ext.asyncio import AsyncSession

from db.config import async_db_session
from db.dal.temperature import TemperatureDAL
from db.models import Temperature
from utils.sync_async_wrappers import force_async
from weather.temperature import CityTemperatureRetriever


async def retrieve_and_store_temperature_for_city(
    latitude: float, longitude: float, city_name: str
):
    temperature_retriever = CityTemperatureRetriever(lat=latitude, lng=longitude)
    temperature_data = await temperature_retriever.retrieve()

    async with async_db_session() as session:
        temperature_dal = TemperatureDAL(session)
        await temperature_dal.insert_multiple_temperatures_for_city(
            temperature_data, city_name
        )


class Correlation:
    @staticmethod
    @force_async
    def _calculate_correlation(temperatures: List[Temperature]) -> float:
        RemotePdb("0.0.0.0", 4444).set_trace()
        temperature_series = []
        altitude_series = []

        for entry in temperatures:
            temperature_series.append(entry.mean)
            altitude_series.append(entry.city.altitude)

        temperature_series = pd.Series(temperature_series)
        altitude_series = pd.Series(altitude_series)

        return altitude_series.corr(temperature_series)

    @classmethod
    async def get_correlation_between_altitude_and_temperature(
        cls, session: AsyncSession
    ) -> float:
        temperature_dal = TemperatureDAL(session)
        results = await temperature_dal.get_temperature_for_all_cities()

        return await cls._calculate_correlation(results)
