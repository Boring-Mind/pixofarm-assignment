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
        await temperature_dal.set_temperature_for_city(
            min=temperature_data.min_temp,
            max=temperature_data.max_temp,
            mean=temperature_data.mean_temp,
            city=city_name,
        )
