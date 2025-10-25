import requests
from app.repository.weather_repo import create_record

from app.config import OWM_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5"
OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"

def fetch_current_weather(location):
    params = {"appid": OWM_KEY, "units": "metric"}
    
    # Check if location is coordinates (lat,lon format)
    if ',' in location:
        try:
            lat, lon = [coord.strip() for coord in location.split(',')]
            # Check if both are valid floats
            float(lat)
            float(lon)
            params["lat"] = lat
            params["lon"] = lon
        except (ValueError, IndexError):
            params["q"] = location
    else:
        params["q"] = location
    
    response = requests.get(f"{BASE_URL}/weather", params=params)
    response.raise_for_status()
    return response.json()

def fetch_5day_forecast(location):
    params = {"appid": OWM_KEY, "units": "metric"}
    
    # Check if location is coordinates (lat,lon format)
    if ',' in location:
        try:
            lat, lon = [coord.strip() for coord in location.split(',')]
            # Check if both are valid floats
            float(lat)
            float(lon)
            params["lat"] = lat
            params["lon"] = lon
        except (ValueError, IndexError):
            params["q"] = location
    else:
        params["q"] = location
    
    response = requests.get(f"{BASE_URL}/forecast", params=params)
    response.raise_for_status()
    data = response.json()

    daily = {}
    for item in data["list"]:
        date = item["dt_txt"].split(" ")[0]
        daily.setdefault(date, []).append(item)
    return daily

# location handling is done in history.py
def fetch_historical_weather(longitude, latitude, start_date, end_date):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m",
        "timezone": "auto"
    }
    
    try:
        response = requests.get(OPEN_METEO_URL, params=params)
        response.raise_for_status()  # raises an error for bad responses
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_weather_record(location, start_date, end_date, weather_json):
    create_record(location, start_date, end_date, weather_json)