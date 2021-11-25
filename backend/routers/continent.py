from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from db.dal.continent import ContinentDAL
from dependencies import get_db_session

router = APIRouter()


@router.get("/continents/", response_class=JSONResponse)
async def get_all_continents(db_session: AsyncSession = Depends(get_db_session)):
    continent_dal = ContinentDAL(db_session)
    return await continent_dal.get_all_continents()
