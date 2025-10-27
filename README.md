# Weather App - Tech Assessment

A comprehensive weather application built for the Product Manager Accelerator (PMA) tech assessment, featuring real-time weather data, 5-day forecasts, CRUD operations, data export, and additional API integrations.

## Features

### Core Weather Features
- **Current Weather**: Real-time weather data with hourly forecasts
- **5-Day Forecast**: Complete weather forecast with visual icons
- **Multiple Location Formats**: Support for cities, postal codes, GPS coordinates, landmarks
- **Google Maps-Style Search**: Advanced search bar with autocomplete suggestions
- **GPS Location Detection**: Automatic location detection using browser geolocation

### Data Management
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality for weather records
- **Database Persistence**: SQLite database for storing weather records
- **Data Validation**: Comprehensive validation for locations and date ranges
- **Enhanced CSV, JSON and .md Export**: Exports actual weather data (date, time, temperature, precipitation, wind speed)

### Additional Integrations
- **YouTube Videos**: Location-related travel and tourism videos
- **Reverse Geocoding**: Converts coordinates to city names using OpenStreetMap Nominatim

### User Experience
- **Auto-loading Integrations**: Location info and media loads automatically
- **Error Handling**: Comprehensive error handling and user feedback

## Technical Stack

### Frontend
- **React.js** - Modern JavaScript framework
- **CSS3** - Styling and responsive design
- **Axios** - HTTP client for API requests

### Backend
- **FastAPI** - Modern Python web framework
- **SQLite** - Lightweight database for data persistence
- **Pydantic** - Data validation and serialization

### APIs & Services
- **Open-Meteo API** - Weather data and geocoding
- **YouTube Data API v3** - Location-related videos (optional)
- **Google Maps API** - Location information (optional)
- **NewsAPI** - Location-related news (optional)

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

## Installation & Setup

### Quick Start (Recommended)

Use the provided startup scripts for easy setup:

**Windows:**
```bash
start.bat
```

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

These scripts will automatically:
- Set up the backend virtual environment
- Install all dependencies
- Start both backend and frontend servers

### Manual Setup

#### Backend Setup

1. **Navigate to the API directory**:
   ```bash
   cd api
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (optional):
   Create a `.env` file in the `api/app/` directory:
   ```bash
   # api/app/.env
   DATABASE_PATH=../data/weather.db
   YOUTUBE_API_KEY=your_youtube_api_key_here
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   NEWS_API_KEY=your_news_api_key_here
   ```

5. **Start the backend server**:
   ```bash
   python -m app.main
   ```
   The API will be available at `http://localhost:8000`

#### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```
   The app will be available at `http://localhost:3000`

## Configuration

### Environment Variables

Create a `.env` file in the `api/app/` directory for optional API keys:

```bash
# api/app/.env
DATABASE_PATH=../data/weather.db
YOUTUBE_API_KEY=your_youtube_api_key_here
```

**Note:** The app works perfectly without these API keys as weather data and core features use the free Open-Meteo API.

### Getting API Keys

1. **YouTube Data API v3**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable YouTube Data API v3
   - Create credentials (API key)

## API Documentation

The backend provides a comprehensive REST API. Visit `http://localhost:8000/docs` for interactive API documentation.

### Key Endpoints

#### Weather Data
- `GET /api/weather/current?location={location}` - Get current weather
- `GET /api/weather/forecast?location={location}` - Get 5-day forecast

#### Weather Records (CRUD)
- `POST /api/weather/history` - Create weather record
- `GET /api/weather/history` - Get all weather records
- `PUT /api/weather/history/{id}` - Update weather record
- `DELETE /api/weather/history/{id}` - Delete weather record

#### Data Export
- `GET /api/weather/export/json` - Export all records as JSON
- `GET /api/weather/export/csv` - Export all records as CSV (with actual weather data)
- `GET /api/weather/export/markdown` - Export all records as Markdown
- `GET /api/weather/export/record/{id}/json` - Export specific record as JSON
- `GET /api/weather/export/record/{id}/csv` - Export specific record as CSV

#### Location Services
- `GET /api/location/search?query={query}` - Search locations with autocomplete
- `GET /api/location/details?latitude={lat}&longitude={lon}` - Get location details (reverse geocoding)

#### Additional Integrations
- `GET /api/location/videos?location={location}` - Get YouTube videos

## Usage Examples

### Current Weather
```
GET /api/weather/current?location=Toronto
GET /api/weather/current?location=M5V3A8
GET /api/weather/current?location=43.6532,-79.3832
```

### 5-Day Forecast
```
GET /api/weather/forecast?location=New York
```

### Create Weather Record
```json
POST /api/weather/history
{
  "location": "London",
  "start_date": "2024-01-01",
  "end_date": "2024-01-07"
}
```

### Export Data
```bash
# Export all records
GET /api/weather/export/json
GET /api/weather/export/csv
GET /api/weather/export/markdown

# Export specific record
GET /api/weather/export/record/1/json
GET /api/weather/export/record/1/csv
```

**CSV Export Format:**
The CSV export includes actual weather data from OpenMeteo API with the following columns:
- Date (YYYY-MM-DD)
- Time (HH:MM)
- Temperature (°C)
- Precipitation (mm)
- Wind Speed (m/s)
- Location

### Location Search
```
GET /api/location/search?query=Toronto
GET /api/location/search?query=New York
GET /api/location/search?query=M5V3A8
GET /api/location/details?latitude=43.6532&longitude=-79.3832
```

## Testing

### Backend Testing
```bash
cd api
python -m pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

## Project Structure

```
weather-app/
├── api/                          # Backend FastAPI application
│   ├── app/
│   │   ├── main.py              # FastAPI app configuration
│   │   ├── config.py            # Configuration settings
│   │   ├── routes/              # API route handlers
│   │   │   ├── current.py       # Current weather endpoints
│   │   │   ├── forecast.py       # Forecast endpoints
│   │   │   ├── history.py       # CRUD operations
│   │   │   ├── export.py        # Data export endpoints
│   │   │   └── integrations.py  # Additional API integrations
│   │   ├── services/            # Business logic
│   │   │   ├── weather_service.py
│   │   │   └── additional_apis.py
│   │   └── repository/          # Data access layer
│   │       ├── db.py
│   │       └── weather_repo.py
│   ├── data/                    # Database files
│   ├── requirements.txt         # Python dependencies
│   └── venv/                   # Virtual environment
├── frontend/                    # React frontend application
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── CurrentWeather.js
│   │   │   ├── Forecast.js
│   │   │   ├── WeatherHistory.js
│   │   │   ├── LocationIntegrations.js
│   │   │   └── PMAInfo.js
│   │   ├── api/                # API client
│   │   │   └── weatherApi.js
│   │   └── App.js              # Main app component
│   ├── package.json            # Node.js dependencies
│   └── public/                # Static assets
├── README.md                   # This file
└── LICENSE                     # License file
```

## Data Validation

The application includes comprehensive data validation:

- **Location Validation**: Supports multiple formats with proper error handling
- **Date Range Validation**: Ensures valid date ranges and formats
- **Coordinate Validation**: Validates latitude/longitude ranges
- **API Response Validation**: Handles API errors gracefully

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

**Backend won't start:**
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify the virtual environment is activated

**Frontend won't start:**
- Ensure Node.js 14+ is installed
- Install dependencies: `npm install`
- Check for port conflicts (default: 3000)

**API errors:**
- Check the API documentation at `http://localhost:8000/docs`
- Verify the backend is running on port 8000
- Check browser console for CORS errors

**Location search not working:**
- Ensure you have an internet connection
- Try different location formats (city name, coordinates, postal code)
- Check browser console for API errors

**YouTube videos not showing:**
- Verify YouTube API key is correctly set in `.env` file
- Check API key permissions in Google Cloud Console
- Ensure the API key has YouTube Data API v3 enabled

**CSV export issues:**
- Ensure you have weather records in the database
- Check that the records contain weather data
- Try exporting individual records first

### Performance Tips

- Use the startup scripts (`start.bat` or `start.sh`) for optimal performance
- Clear browser cache if experiencing UI issues
- Restart both servers if encountering persistent errors