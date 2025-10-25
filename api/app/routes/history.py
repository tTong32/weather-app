from fastapi import APIRouter, Query, HTTPException, Path
from pydantic import BaseModel, validator
from datetime import datetime
import json

from app.repository import weather_repo
from app.services import weather_service
from app.services.weather_service import fetch_historical_weather

router = APIRouter()

class CreateWeatherRequest(BaseModel):
    location: str
    start_date: str
    end_date: str
    
class UpdateWeatherRequest(BaseModel):
    location: str = None
    start_date: str = None
    end_date: str = None

def get_coordinates(location):
    """
    Convert location string to lat/lon coordinates.
    Handles coordinates (43.65,-79.38) or city names (Toronto).
    """
    if ',' in location:
        try:
            lat, lon = [coord.strip() for coord in location.split(',')]
            lat = float(lat)
            lon = float(lon)
            return lat, lon
        except (ValueError, IndexError):
            pass
    try:
        weather_data = weather_service.fetch_current_weather(location)
        lat = weather_data['coord']['lat']
        lon = weather_data['coord']['lon']
        return lat, lon
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid location: {str(e)}")

@router.post("/history", summary="Create a new weather record")
def create_record(request: CreateWeatherRequest):
    # TODO: add location and time validation
    try:
        latitude, longitude = get_coordinates(request.location)
        print(f"Latitude: {latitude}, Longitude: {longitude}")
        data = fetch_historical_weather(longitude, latitude, request.start_date, request.end_date)
        if data:
            weather_json = json.dumps(data)
            weather_repo.create_record(request.location, request.start_date, request.end_date, weather_json)
            return {"status": "success", "message": "Weather record created successfully"}
        else:
            return {"status": "error", "message": "Failed to fetch weather data"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/history", summary="Get all weather records")
def get_all_records():
    try: 
        records = weather_repo.read_all_records()
        return {"status": "success", "data": records}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/history/{record_id}", summary="Update a weather record")
def update_record(record_id: int, request: UpdateWeatherRequest):
    try:
        record = weather_repo.return_record(record_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Record not found")
        
        location = request.location if request.location is not None else record['location']
        start_date = request.start_date if request.start_date is not None else record['start_date']
        end_date = request.end_date if request.end_date is not None else record['end_date']
        
        should_fetch = (
            request.location is not None or
            request.start_date is not None or
            request.end_date is not None
        )
        
        if should_fetch:
            latitude, longitude = get_coordinates(location)
            data = fetch_historical_weather(longitude, latitude, start_date, end_date)
            
            if data:
                weather_json = json.dumps(data)
            else:
                raise HTTPException(status_code=400, detail="Failed to fetch weather data")
        else:
            weather_json = record['weather_json']
        
        weather_repo.update_record(record_id, location, start_date, end_date, weather_json)
        
        return {"status": "success", "message": "Weather record updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/history/{record_id}", summary="Delete a weather record")
def delete_record(record_id: int):
    try:
        weather_repo.delete_record(record_id)
        return {"status": "success", "message": "Weather record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
