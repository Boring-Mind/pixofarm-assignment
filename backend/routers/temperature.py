from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from db.dal.temperature import TemperatureDAL
from dependencies import get_db_session

router = APIRouter()


@router.get("/temperatures/city/{city_id}/", response_class=JSONResponse)
async def get_all_cities(
    city_id: int, db_session: AsyncSession = Depends(get_db_session)
):
    temperature_dal = TemperatureDAL(db_session)
    return await temperature_dal.get_temperature_for_city_id(city_id)
