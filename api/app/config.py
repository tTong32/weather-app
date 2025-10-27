import os
from pathlib import Path

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/weather.db")

# Ensure data directory exists
Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)