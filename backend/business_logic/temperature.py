from db.config import async_db_session
from db.dal.temperature import TemperatureDAL
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


# class Correlation:
#     @staticmethod
#     @force_async
#     def _calculate_correlation(retrieved_data_from_db) -> float:
#         temperature_series, altitude_series = retrieved_data_from_db
#         temperature_series = []
#         altitude_series = []
#
#         for entry in temperature_list:
#             temperature_series.append(entry.mean)
#
#         temperature_series = pd.Series(temperature_series)
#         altitude_series = pd.Series(altitude_series)
#
#         return altitude_series.corr(temperature_series)
#
#     @classmethod
#     @force_async
#     def combine_cities_with_temperatures(
#         cls, cities: List[City], temperatures: List[Temperature]
#     ) -> Tuple[List[Temperature], List[int]]:
#         city_dict = {c.id: c.altitude for c in cities}
#
#         altitudes_list = []
#         for t in temperatures:
#             altitudes_list.append(city_dict[t.city])
#
#         return temperatures, altitudes_list
#
#     @classmethod
#     async def get_correlation_between_altitude_and_temperature(
#         cls, session: AsyncSession
#     ) -> float:
#         temperature_dal = TemperatureDAL(session)
#         temperatures = await temperature_dal.get_all_temperatures()
#
#         city_dal = CityDAL(session)
#         cities = await city_dal.get_all_cities()
#
#         results = await cls.combine_cities_with_temperatures(cities, temperatures)
#
#         return await cls._calculate_correlation(results)
