import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file in root

OWM_KEY = os.getenv("OWM_KEY")
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/weather.db")