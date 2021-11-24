from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Continent


class ContinentDAL:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_all_continents(self) -> Optional[List[Continent]]:
        results = await self.session.execute(select(Continent))
        return results.scalars().all()
