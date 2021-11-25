from typing import List, Optional

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.dal.continent import ContinentDAL
from db.models import City


class CityDAL:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_all_cities(self) -> Optional[List[City]]:
        results = await self.session.execute(select(City))
        return results.scalars().all()

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
