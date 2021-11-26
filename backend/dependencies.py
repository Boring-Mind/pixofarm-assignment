from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from redis_connection import redis_connection_pool
from db.config import async_db_session


async def get_db_session() -> AsyncSession:
    async with async_db_session() as session:
        yield session


async def redis_instance() -> Redis:
    yield Redis(connection_pool=redis_connection_pool)
