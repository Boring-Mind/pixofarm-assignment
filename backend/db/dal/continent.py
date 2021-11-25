from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Continent


class ContinentNotFound(Exception):
    _default_message: str = "Cannot find a continent with that name"


class ContinentDAL:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_all_continents(self) -> Optional[List[Continent]]:
        results = await self.session.execute(select(Continent))
        return results.scalars().all()

    async def get_continent_by_name(self, name: str) -> Continent:
        results = await self.session.execute(
            select(Continent).where(Continent.name == name)
        )
        continent = results.scalars().first()

        if continent is None:
            raise ContinentNotFound

        return continent
