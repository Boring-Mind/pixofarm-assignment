from sqlalchemy.ext.asyncio import AsyncSession

from db.config import async_db_session


async def get_db_session() -> AsyncSession:
    async with async_db_session() as session:
        yield session
