from typing import Optional, List, Iterable

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.dal.city import CityDAL
from db.models import Temperature, City


class TemperatureDAL:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_temperature_for_cities(
        self, city_names: Iterable[str]
    ) -> Optional[List[Temperature]]:
        query = (
            select(Temperature)
            .join(City, Temperature.city == City.id)
            .filter(City.name.in_(city_names))
        )
        results = await self.session.execute(query)
        return results.scalars().all()

    async def set_temperature_for_city(
        self, min: float, max: float, mean: float, city: str | int
    ):
        if isinstance(city, str):
            city_dal = CityDAL(self.session)
            city = await city_dal.get_city_by_name(city)

        query = insert(Temperature).values(min=min, max=max, mean=mean, city=city)

        await self.session.execute(query)
        await self.session.commit()
