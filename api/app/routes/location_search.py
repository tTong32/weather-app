from fastapi import APIRouter, Query, HTTPException
from typing import List

from app.services.location_search import search_locations, get_location_details

router = APIRouter()

@router.get("/search", summary="Search for locations with autocomplete")
def search_locations_endpoint(
    query: str = Query(..., description="Search query for location", min_length=2),
    limit: int = Query(5, description="Maximum number of results", ge=1, le=10)
):
    """
    Search for locations using Open-Meteo geocoding API.
    Returns location suggestions for autocomplete functionality.
    """
    try:
        locations = search_locations(query, limit)
        return {
            "status": "success",
            "data": {
                "query": query,
                "locations": locations,
                "total_results": len(locations)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search locations: {str(e)}")

@router.get("/details", summary="Get detailed information about a location")
def get_location_details_endpoint(
    latitude: float = Query(..., description="Latitude coordinate"),
    longitude: float = Query(..., description="Longitude coordinate")
):
    """
    Get detailed information about a specific location using coordinates.
    """
    try:
        details = get_location_details(latitude, longitude)
        if not details:
            raise HTTPException(status_code=404, detail="Location not found")
        
        return {
            "status": "success",
            "data": details
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get location details: {str(e)}")
