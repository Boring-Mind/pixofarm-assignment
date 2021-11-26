from typing import List

from aioredis import Redis
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from business_logic.temperature import Correlation
from db.dal.temperature import TemperatureDAL
from dependencies import get_db_session, redis_instance
from settings import Settings

router = APIRouter()


@router.get("/temperature/city/{city_id}/", response_class=JSONResponse)
async def get_temperature_for_the_city(
    city_id: int, db_session: AsyncSession = Depends(get_db_session)
):
    temperature_dal = TemperatureDAL(db_session)
    return await temperature_dal.get_temperature_for_city_id(city_id)


@router.get("/temperature/cities/", response_class=JSONResponse)
async def get_temperature_for_specified_cities(
    city_names: List[str] = Query(None),
    db_session: AsyncSession = Depends(get_db_session),
):
    temperature_dal = TemperatureDAL(db_session)
    return await temperature_dal.get_temperature_for_cities(city_names)


@router.get("/temperature/correlation/", response_class=JSONResponse)
async def get_correlation_between_temperature_and_altitude(
    db_session: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(redis_instance),
):
    if cached_result := await redis.get(Settings.CORRELATION_CACHE_KEY):
        return cached_result

    # ToDo: fix issues with non-consumed column
    # ToDo: research more about sqlalchemy relationship
    result = await Correlation.get_correlation_between_altitude_and_temperature(
        db_session
    )
    await redis.set(
        Settings.CORRELATION_CACHE_KEY, result, ex=Settings.CORRELATION_CACHE_EXP
    )
    return {"correlation": str(result)}
