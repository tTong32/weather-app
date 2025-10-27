import requests
from app.repository.weather_repo import create_record

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

def get_weather_icon(weather_code):
    """Map Open-Meteo weather codes to emoji icons"""
    weather_icons = {
        0: "☀️",   # Clear sky
        1: "🌤️",   # Mainly clear
        2: "⛅",    # Partly cloudy
        3: "☁️",    # Overcast
        45: "🌫️",  # Fog
        48: "🌫️",  # Depositing rime fog
        51: "🌦️",  # Light drizzle
        53: "🌦️",  # Moderate drizzle
        55: "🌧️",  # Dense drizzle
        56: "🌨️",  # Light freezing drizzle
        57: "🌨️",  # Dense freezing drizzle
        61: "🌧️",  # Slight rain
        63: "🌧️",  # Moderate rain
        65: "🌧️",  # Heavy rain
        66: "🌨️",  # Light freezing rain
        67: "🌨️",  # Heavy freezing rain
        71: "❄️",  # Slight snow fall
        73: "❄️",  # Moderate snow fall
        75: "❄️",  # Heavy snow fall
        77: "❄️",  # Snow grains
        80: "🌦️",  # Slight rain showers
        81: "🌧️",  # Moderate rain showers
        82: "🌧️",  # Violent rain showers
        85: "🌨️",  # Slight snow showers
        86: "🌨️",  # Heavy snow showers
        95: "⛈️",  # Thunderstorm
        96: "⛈️",  # Thunderstorm with slight hail
        99: "⛈️"   # Thunderstorm with heavy hail
    }
    return weather_icons.get(weather_code, "🌤️")

def get_weather_description(weather_code):
    """Map Open-Meteo weather codes to descriptions"""
    weather_descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_descriptions.get(weather_code, "Unknown")

def geocode_location(location):
    """Convert location string to coordinates using geocoding"""
    if not location or not location.strip():
        raise ValueError("Location cannot be empty")
    
    location = location.strip()
    
    # Handle coordinate input (lat,lon)
    if ',' in location:
        try:
            parts = [coord.strip() for coord in location.split(',')]
            if len(parts) != 2:
                raise ValueError("Coordinates must be in format 'latitude,longitude'")
            
            lat, lon = float(parts[0]), float(parts[1])
            
            # Validate coordinate ranges
            if not (-90 <= lat <= 90):
                raise ValueError("Latitude must be between -90 and 90 degrees")
            if not (-180 <= lon <= 180):
                raise ValueError("Longitude must be between -180 and 180 degrees")
            
            return lat, lon
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid coordinate format: {str(e)}")
    
    # Handle postal code (basic validation)
    if location.isdigit() and len(location) >= 3:
        # Likely a postal code
        pass
    elif len(location) < 2:
        raise ValueError("Location must be at least 2 characters long")
    
    # Geocode the location using Open-Meteo geocoding API
    params = {"name": location, "count": 1}
    try:
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("results"):
            result = data["results"][0]
            return result["latitude"], result["longitude"]
        else:
            raise ValueError(f"Location '{location}' not found. Please check spelling or try a different format.")
            
    except requests.exceptions.Timeout:
        raise ValueError("Location lookup timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to lookup location: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error during geocoding: {str(e)}")

def fetch_current_weather(location):
    """Fetch current weather with hourly data from Open-Meteo"""
    lat, lon = geocode_location(location)
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code",
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,apparent_temperature,weather_code",
        "timezone": "auto"
    }
    
    response = requests.get(OPEN_METEO_URL, params=params)
    response.raise_for_status()
    data = response.json()
    
    # Get current data
    current = data.get("current", {})
    hourly = data.get("hourly", {})
    
    # Calculate min/max from today's hourly data
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    
    # Get today's data (first 24 hours)
    today_times = times[:24] if times else []
    today_temps = temps[:24] if temps else []
    today_humidity = hourly.get("relative_humidity_2m", [])[:24]
    today_precip = hourly.get("precipitation", [])[:24]
    today_wind = hourly.get("wind_speed_10m", [])[:24]
    today_weather_codes = hourly.get("weather_code", [])[:24]
    
    current_weather_code = current.get("weather_code")
    
    return {
        "location": location,
        "current_temp": current.get("temperature_2m"),
        "feels_like": current.get("apparent_temperature"),
        "high": max(today_temps) if today_temps else current.get("temperature_2m"),
        "low": min(today_temps) if today_temps else current.get("temperature_2m"),
        "average": sum(today_temps) / len(today_temps) if today_temps else current.get("temperature_2m"),
        "hourly_times": today_times,
        "hourly_temperature": temps[:24],
        "hourly_humidity": today_humidity,
        "hourly_precipitation": today_precip,
        "hourly_wind": today_wind,
        "hourly_weather_codes": today_weather_codes,
        "current_humidity": current.get("relative_humidity_2m"),
        "current_precipitation": current.get("precipitation"),
        "current_wind": current.get("wind_speed_10m"),
        "current_weather_code": current_weather_code,
        "current_weather_icon": get_weather_icon(current_weather_code),
        "current_weather_description": get_weather_description(current_weather_code),
        "latitude": lat,
        "longitude": lon
    }

def fetch_5day_forecast(location):
    """Fetch 5-day forecast from Open-Meteo"""
    lat, lon = geocode_location(location)
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,wind_speed_10m_max,weather_code",
        "timezone": "auto"
    }
    
    response = requests.get(OPEN_METEO_URL, params=params)
    response.raise_for_status()
    data = response.json()
    
    daily = data.get("daily", {})
    
    forecast = []
    dates = daily.get("time", [])
    temps_max = daily.get("temperature_2m_max", [])
    temps_min = daily.get("temperature_2m_min", [])
    temps_avg = daily.get("temperature_2m_mean", [])
    precipitation = daily.get("precipitation_sum", [])
    wind = daily.get("wind_speed_10m_max", [])
    weather_codes = daily.get("weather_code", [])
    
    for i in range(min(len(dates), 5)):  # Get 5 days
        weather_code = weather_codes[i]
        forecast.append({
            "date": dates[i],
            "temp_max": temps_max[i],
            "temp_min": temps_min[i],
            "temp_avg": temps_avg[i],
            "precipitation": precipitation[i],
            "wind_speed": wind[i],
            "weather_code": weather_code,
            "weather_icon": get_weather_icon(weather_code),
            "weather_description": get_weather_description(weather_code)
        })
    
    return {"location": location, "forecast": forecast}

# Historical weather for CRUD operations
def fetch_historical_weather(longitude, latitude, start_date, end_date):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,precipitation,wind_speed_10m",
        "timezone": "auto"
    }
    
    try:
        response = requests.get("https://archive-api.open-meteo.com/v1/archive", params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_weather_record(location, start_date, end_date, weather_json):
    create_record(location, start_date, end_date, weather_json)