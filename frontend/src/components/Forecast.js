import React, { useState } from 'react';
import { getForecast } from '../api/weatherApi';
import LocationSearchBar from './LocationSearchBar';
import './Forecast.css';

function Forecast() {
  const [location, setLocation] = useState('');
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (searchLocation = location) => {
    if (!searchLocation.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await getForecast(searchLocation);
      setForecast(data.data.forecast);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch forecast');
      setForecast(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLocationSelect = (selectedLocation) => {
    handleSearch(selectedLocation);
  };

  return (
    <div className="forecast">
      <h2>5-Day Forecast</h2>
      
      <div className="search-container">
        <LocationSearchBar 
          onLocationSelect={handleLocationSelect}
          placeholder="Search for a location..."
        />
      </div>

      {loading && <div className="loading">Loading...</div>}
      
      {error && <div className="error">{error}</div>}

      {forecast && (
        <div className="forecast-grid">
          {forecast.map((day, index) => (
            <div key={index} className="forecast-card">
              <div className="forecast-date">
                {new Date(day.date).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}
              </div>
              
              <div className="forecast-icon">{day.weather_icon}</div>
              <div className="forecast-condition">{day.weather_description}</div>
              
              <div className="forecast-temps">
                <div className="temp-max">{day.temp_max?.toFixed(0)}°</div>
                <div className="temp-avg">{day.temp_avg?.toFixed(0)}°</div>
                <div className="temp-min">{day.temp_min?.toFixed(0)}°</div>
              </div>

              <div className="forecast-details">
                <div className="detail-row">
                  <span className="detail-icon">💨</span>
                  <span>{day.wind_speed?.toFixed(1)} km/h</span>
                </div>
                <div className="detail-row">
                  <span className="detail-icon">🌧️</span>
                  <span>{day.precipitation?.toFixed(1)} mm</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Forecast;
