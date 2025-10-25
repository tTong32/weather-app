from fastapi import FastAPI
from weather_api import current, forecast
from repository.db import init_db

app = FastAPI(title="Weather App API")

# initialize SQLite DB
init_db()

# register routers
app.include_router(current.router, prefix="/api/weather")
app.include_router(forecast.router, prefix="/api/weather")
