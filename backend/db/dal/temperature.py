from datetime import datetime
from typing import Optional, List, Iterable

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.dal.city import CityDAL
from db.models import Temperature, City
from weather.temperature import TemperatureData


class TemperatureDAL:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def _get_temperature_for_(self, query) -> Optional[List[Temperature]]:
        results = await self.session.execute(query)
        return results.scalars().all()

    async def get_temperature_for_city_id(
        self, city_id: int
    ) -> Optional[List[Temperature]]:
        return await self._get_temperature_for_(
            select(Temperature).filter(Temperature.city == city_id)
        )

    async def get_temperature_for_cities(
        self, city_names: Iterable[str]
    ) -> Optional[List[Temperature]]:
        query = (
            select(Temperature)
            .join(City, Temperature.city == City.id)
            .filter(City.name.in_(city_names))
        )
        return await self._get_temperature_for_(query)

    async def set_temperature_for_city(
        self, min: float, max: float, mean: float, date: datetime, city: str | int
    ):
        if isinstance(city, str):
            city_dal = CityDAL(self.session)
            city = await city_dal.get_city_by_name(city)
            city = city.id

        query = insert(Temperature).values(
            min=min, max=max, mean=mean, date=date, city=city
        )

        await self.session.execute(query)
        await self.session.commit()

    async def insert_multiple_temperatures_for_city(
        self, temperature_list: List[TemperatureData], city: str | int
    ):
        if isinstance(city, str):
            city_dal = CityDAL(self.session)
            city = await city_dal.get_city_by_name(city)
            city = city.id

        query = insert(Temperature).values(
            [t.to_db_dict() | {"city": city} for t in temperature_list]
        )

        await self.session.execute(query)
        await self.session.commit()
