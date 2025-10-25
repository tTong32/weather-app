from fastapi import APIRouter
from services.weather_service import fetch_current_weather, save_weather_record

router = APIRouter()

@router.get("/current")
def get_current(location: str):
    data = fetch_current_weather(location)
    save_weather_record(location, None, None, str(data))
    return {"status": "success", "data": data}