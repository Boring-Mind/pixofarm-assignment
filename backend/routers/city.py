from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from business_logic.temperature import retrieve_and_store_temperature_for_city
from db.dal.city import CityDAL
from db.dal.continent import ContinentNotFound
from dependencies import get_db_session
from pydantic_models.routers.city import CreateCityIn

router = APIRouter()


@router.get("/cities/", response_class=JSONResponse)
async def get_all_cities(db_session: AsyncSession = Depends(get_db_session)):
    continent_dal = CityDAL(db_session)
    return await continent_dal.get_all_cities()


@router.delete("/city/{city_id}/")
async def delete_city(
    city_id: int,
    db_session: AsyncSession = Depends(get_db_session),
):
    city_dal = CityDAL(db_session)
    await city_dal.delete_city_by_id(city_id)
    return JSONResponse(
        {"message": "Successfully deleted city"}, status_code=status.HTTP_204_NO_CONTENT
    )


@router.post("/city/", response_class=JSONResponse)
async def create_city(
    input_data: CreateCityIn,
    db_session: AsyncSession = Depends(get_db_session),
):
    city_dal = CityDAL(db_session)
    try:
        await city_dal.create_new_city(
            name=input_data.name,
            latitude=input_data.latitude,
            longitude=input_data.longitude,
            altitude=input_data.altitude,
            continent=input_data.continent,
        )

        await retrieve_and_store_temperature_for_city(
            latitude=input_data.latitude,
            longitude=input_data.longitude,
            city_name=input_data.name,
        )

        return JSONResponse(
            {"message": "Created city"}, status_code=status.HTTP_201_CREATED
        )
    except ContinentNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot find specified continent",
        )
