from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from db.dal.temperature import TemperatureDAL
from dependencies import get_db_session

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