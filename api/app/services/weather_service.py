import requests
from repository.weather_repo import create_record

from config import OWM_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5"

def fetch_current_weather(location):
    params = {"q": location, "appid": OWM_KEY, "units": "metric"}
    response = requests.get(f"{BASE_URL}/weather", params=params)
    response.raise_for_status()
    return response.json()

def fetch_5day_forecast(location):
    params = {"q": location, "appid": OWM_KEY, "units": "metric"}
    response = requests.get(f"{BASE_URL}/forecast", params=params)
    response.raise_for_status()
    data = response.json()
    # optional: group by day
    daily = {}
    for item in data["list"]:
        date = item["dt_txt"].split(" ")[0]
        daily.setdefault(date, []).append(item)
    return daily

def save_weather_record(location, start_date, end_date, weather_json):
    create_record(location, start_date, end_date, weather_json)
