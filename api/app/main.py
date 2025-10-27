from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from app.routes.current import router as current_router
from app.routes.forecast import router as forecast_router
from app.routes.history import router as history_router
from app.routes.export import router as export_router
from app.routes.integrations import router as integrations_router
from app.routes.location_search import router as location_search_router

from app.repository.db import init_db

app = FastAPI(title="Weather App API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"(http://localhost:?.*|https://.*\.railway\.app|https://.*\.vercel\.app|https://.*\.netlify\.app|https://.*\.onrender\.com|https://weather-app-frontend-y3t2\.onrender\.com)",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(current_router, prefix="/api/weather")
app.include_router(forecast_router, prefix="/api/weather")
app.include_router(history_router, prefix="/api/weather")
app.include_router(export_router, prefix="/api/weather")
app.include_router(integrations_router, prefix="/api")
app.include_router(location_search_router, prefix="/api/location")


@app.get("/")
def root():
    return {"status": "ok", "message": "Weather API - try /api/weather/current?location=Toronto"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)