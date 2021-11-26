from typing import List, Optional

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from common_exceptions import CommonException
from db.dal.continent import ContinentDAL
from db.models import City


class CityNotFound(CommonException):
    _default_message: str = "Cannot find a city with the specified name."


class CityDAL:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_all_cities(self) -> Optional[List[City]]:
        results = await self.session.execute(select(City))
        return results.scalars().all()

    async def get_city_by_name(self, name: str) -> City:
        results = await self.session.execute(select(City).where(City.name == name))
        city = results.scalars().first()

        if not city:
            raise CityNotFound

        return city

    async def delete_city_by_id(self, city_id: int):
        query = delete(City).where(City.id == city_id)
        await self.session.execute(query)
        await self.session.commit()

    async def create_new_city(
        self,
        name: str,
        latitude: float,
        longitude: float,
        altitude: float,
        continent: int | str,
    ):
        """Create a new city.

        If the continent is a string then we'll find a continent id in our DB
        by continents' name.
        """
        if isinstance(continent, str):
            continent_dal = ContinentDAL(self.session)
            continent = await continent_dal.get_continent_by_name(continent)

        query = insert(City).values(
            name=name,
            latitude=latitude,
            longitude=longitude,
            altitude=altitude,
            continent=continent,
        )

        await self.session.execute(query)
        await self.session.commit()
