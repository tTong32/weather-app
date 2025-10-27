from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.weather_service import fetch_5day_forecast
from app.repository import weather_repo

import traceback
from datetime import datetime, timezone

router = APIRouter()

@router.get("/forecast", summary="Get 5-day forecast for a location")
def get_forecast(location: str = Query(..., description="City name, postal code, landmark, or 'lat,lon' coordinates")):
    """
    Example: /api/weather/forecast?location=Toronto
    Returns 5-day forecast from Open-Meteo with temps, precipitation, and wind
    """
    try:
        data = fetch_5day_forecast(location)
        
        return {"status": "success", "data": data}
        
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Could not fetch forecast for '{location}': {str(exc)}")
