from fastapi import APIRouter
from services.weather_service import fetch_5day_forecast

router = APIRouter()

@router.get("/forecast")
def get_forecast(location: str):
    data = fetch_5day_forecast(location)
    return {"status": "success", "data": data}
