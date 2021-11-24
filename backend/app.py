from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from db.dal.continent import ContinentDAL
from dependencies import get_db_session

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/test-db/", response_class=JSONResponse)
async def test_db(db_session: AsyncSession = Depends(get_db_session)):
    continent_dal = ContinentDAL(db_session)
    return await continent_dal.get_all_continents()
