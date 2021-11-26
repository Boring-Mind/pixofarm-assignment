from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers.continent import router as continent_router
from routers.city import router as city_router
from routers.temperature import router as temperature_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(continent_router)
app.include_router(city_router)
app.include_router(temperature_router)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
