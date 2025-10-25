from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from app.services import weather_service
from app.repository import weather_repo # optional later for saving

import traceback
from datetime import datetime, timezone

router = APIRouter()

@router.get("/current", summary="Get current weather for a location")
def get_current(location: str = Query(..., description="City name, postal code, landmark, or 'lat,lon' coordinates")):
    """
    Example: /api/weather/current?location=Toronto
    """
    try:
        data = weather_service.fetch_current_weather(location)

        weather = {
            "location": f"{data.get('name', '')}, {data.get('sys', {}).get('country', '')}".strip(", "),
            "temperature": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "humidity": data.get("main", {}).get("humidity"),
            "wind_speed": data.get("wind", {}).get("speed"),
            "condition": (data.get("weather") or [{}])[0].get("description", "").title(),
            "icon": (data.get("weather") or [{}])[0].get("icon"),
            "timestamp": datetime.fromtimestamp(data.get("dt", 0), tz=timezone.utc).isoformat().replace("+00:00", "Z")
        }

        return {"status": "success", "data": weather}

    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Could not fetch weather for '{location}': {str(exc)}")

    