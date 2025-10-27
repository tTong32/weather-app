from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from app.services.additional_apis import additional_api_service

router = APIRouter()

@router.get("/location/videos", summary="Get YouTube videos related to a location")
def get_location_videos(
    location: str = Query(..., description="Location to search videos for"),
    max_results: int = Query(5, description="Maximum number of videos to return", ge=1, le=10)
):
    """
    Get YouTube videos related to a specific location.
    Requires YouTube Data API v3 key to be configured.
    """
    try:
        result = additional_api_service.get_location_videos(location, max_results)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch videos: {str(e)}")

@router.get("/location/integrations", summary="Get all available integrations for a location")
def get_location_integrations(
    location: str = Query(..., description="Location to get integrations for")
):
    """
    Get all available integrations (YouTube) for a location.
    """
    try:
        videos_result = additional_api_service.get_location_videos(location, 3)
        
        return {
            "status": "success",
            "data": {
                "location": location,
                "youtube": videos_result,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch integrations: {str(e)}")
