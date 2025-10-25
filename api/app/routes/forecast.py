from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.weather_service import fetch_5day_forecast
from app.repository import weather_repo # optional later for saving

import traceback
from datetime import datetime, timezone

router = APIRouter()

def average(values):
    return sum(values) / len(values) if values else None

def get_mode(values):
    if not values:
        return None
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return max(counts, key=counts.get)

@router.get("/forecast", summary="Get 5-day forecast for a location")
def get_forecast(location: str = Query(..., description="City name, postal code, or 'lat,lon'")):
    """
    Example: /api/weather/forecast?location=Toronto
    """
    try:
        daily_grouped = fetch_5day_forecast(location)
        
        forecast_list = []
        for date, hourly_data in daily_grouped.items():
            if hourly_data:  # Make sure there's data
                # Get first reading of the day for summary
                first_reading = hourly_data[0]
                
                # Calculate min/max temps from all readings that day
                temps = [item.get("main", {}).get("temp") for item in hourly_data if item.get("main", {}).get("temp")]
                temp_min = min(temps) if temps else None
                temp_max = max(temps) if temps else None

                humidity = average([item.get("main", {}).get("humidity") for item in hourly_data if item.get("main", {}).get("humidity")])
                max_wind_speed = max([item.get("wind", {}).get("speed") for item in hourly_data if item.get("wind", {}).get("speed")])
                feels_like = average([item.get("main", {}).get("feels_like") for item in hourly_data if item.get("main", {}).get("feels_like")])
                condition = get_mode([item.get("weather", [{}])[0].get("description", "").title() for item in hourly_data])
                
                forecast_item = {
                    "date": date,
                    "temp_min": temp_min,
                    "temp_max": temp_max,
                    "condition": condition,
                    "humidity": humidity,
                    "wind_speed": max_wind_speed,
                    "feels_like": feels_like,
                    "icon": (first_reading.get("weather") or [{}])[0].get("icon"),
                }
                forecast_list.append(forecast_item)
        
        # Sort by date to ensure chronological order
        forecast_list.sort(key=lambda x: x["date"])
        
        return {"status": "success", "location": location, "forecast": forecast_list}
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Could not fetch forecast for '{location}': {str(exc)}")
