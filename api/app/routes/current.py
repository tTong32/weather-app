from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from app.services import weather_service
from app.repository import weather_repo

import traceback
from datetime import datetime, timezone

router = APIRouter()

@router.get("/current", summary="Get current weather for a location")
def get_current(location: str = Query(..., description="City name, postal code, landmark, or 'lat,lon' coordinates")):
    """
    Example: /api/weather/current?location=Toronto
    Returns current weather with hourly data from Open-Meteo
    """
    try:
        data = weather_service.fetch_current_weather(location)
        
        # Return the data directly as it's already properly formatted
        return {"status": "success", "data": data}

    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Could not fetch weather for '{location}': {str(exc)}")

    