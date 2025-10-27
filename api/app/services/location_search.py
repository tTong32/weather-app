import requests
from typing import List, Dict, Any
from app.services.weather_service import GEOCODING_URL

def search_locations(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Search for locations using Open-Meteo geocoding API
    Returns a list of location suggestions with details
    """
    if not query or len(query.strip()) < 2:
        return []
    
    try:
        params = {
            "name": query.strip(),
            "count": limit,
            "language": "en",
            "format": "json"
        }
        
        response = requests.get(GEOCODING_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        locations = []
        for result in data.get("results", []):
            location_info = {
                "name": result.get("name", ""),
                "country": result.get("country", ""),
                "admin1": result.get("admin1", ""),  # State/Province
                "admin2": result.get("admin2", ""),  # County
                "latitude": result.get("latitude", 0),
                "longitude": result.get("longitude", 0),
                "display_name": format_location_name(result),
                "search_query": f"{result.get('latitude')},{result.get('longitude')}"
            }
            locations.append(location_info)
        
        return locations
        
    except requests.exceptions.RequestException:
        return []
    except Exception:
        return []

def format_location_name(result: Dict[str, Any]) -> str:
    """
    Format location name for display in search suggestions
    """
    name = result.get("name", "")
    country = result.get("country", "")
    admin1 = result.get("admin1", "")
    
    # Build display name
    parts = [name]
    
    if admin1 and admin1 != name:
        parts.append(admin1)
    
    if country and country not in parts:
        parts.append(country)
    
    return ", ".join(parts)

def get_location_details(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get detailed information about a specific location using reverse geocoding
    Uses OpenStreetMap Nominatim API for reverse geocoding
    """
    try:
        # Use OpenStreetMap Nominatim for reverse geocoding
        nominatim_url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "json",
            "addressdetails": 1,
            "accept-language": "en"
        }
        
        headers = {
            "User-Agent": "WeatherApp/1.0"  # Required by Nominatim
        }
        
        response = requests.get(nominatim_url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data and data.get("address"):
            address = data["address"]
            return {
                "name": address.get("city") or address.get("town") or address.get("village") or address.get("hamlet") or "Unknown",
                "country": address.get("country", ""),
                "admin1": address.get("state") or address.get("province") or "",
                "admin2": address.get("county") or "",
                "latitude": latitude,
                "longitude": longitude,
                "display_name": data.get("display_name", ""),
                "timezone": "",  # Nominatim doesn't provide timezone
                "population": 0   # Nominatim doesn't provide population
            }
        
        return {}
        
    except Exception:
        return {}
