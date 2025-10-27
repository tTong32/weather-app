import React, { useState } from 'react';
import { getCurrentWeather } from '../api/weatherApi';
import LocationSearchBar from './LocationSearchBar';
import LocationIntegrations from './LocationIntegrations';
import './CurrentWeather.css';

function CurrentWeather() {
  const [location, setLocation] = useState('');
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (searchLocation = location) => {
    if (!searchLocation.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await getCurrentWeather(searchLocation);
      setWeather(data.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch weather');
      setWeather(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLocationSelect = (selectedLocation) => {
    handleSearch(selectedLocation);
  };

  const handleGetLocation = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser');
      return;
    }

    setLoading(true);
    setError(null);

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        const coords = `${latitude},${longitude}`;
        
        try {
          const data = await getCurrentWeather(coords);
          setWeather(data.data);
        } catch (err) {
          setError(err.response?.data?.detail || 'Failed to fetch weather');
        } finally {
          setLoading(false);
        }
      },
      (error) => {
        setError('Location access denied');
        setLoading(false);
      }
    );
  };

  return (
    <div className="current-weather">
      <h2>Current Weather</h2>
      
      <div className="search-container">
        <LocationSearchBar 
          onLocationSelect={handleLocationSelect}
          placeholder="Search for a city, postal code, landmark, or coordinates..."
        />
        <button onClick={handleGetLocation} className="location-btn" disabled={loading}>
          📍 Use My Location
        </button>
      </div>

      {loading && <div className="loading">Loading...</div>}
      
      {error && <div className="error">{error}</div>}

      {weather && (
        <div className="weather-card">
          <div className="weather-header">
            <h3>{weather.location}</h3>
          </div>
          
          <div className="weather-main">
            <div className="weather-icon-large">{weather.current_weather_icon}</div>
            <div className="temperature">{weather.current_temp?.toFixed(1)}°C</div>
            <div className="condition">{weather.current_weather_description}</div>
            <div className="feels-like">Feels like {weather.feels_like?.toFixed(1)}°C</div>
          </div>

          <div className="temp-summary">
            <div className="temp-item">
              <span className="label">High:</span>
              <span className="value">{weather.high?.toFixed(1)}°C</span>
            </div>
            <div className="temp-item">
              <span className="label">Low:</span>
              <span className="value">{weather.low?.toFixed(1)}°C</span>
            </div>
            <div className="temp-item">
              <span className="label">Average:</span>
              <span className="value">{weather.average?.toFixed(1)}°C</span>
            </div>
          </div>

          <div className="weather-details">
            <div className="detail-item">
              <span className="label">Humidity:</span>
              <span>{weather.current_humidity}%</span>
            </div>
            <div className="detail-item">
              <span className="label">Wind Speed:</span>
              <span>{weather.current_wind?.toFixed(1)} km/h</span>
            </div>
            <div className="detail-item">
              <span className="label">Precipitation:</span>
              <span>{weather.current_precipitation?.toFixed(1)} mm</span>
            </div>
          </div>

          {weather.hourly_temperature && weather.hourly_temperature.length > 0 && (
            <div className="hourly-section">
              <h4>Hourly Data (Today)</h4>
              <div className="hourly-grid">
                <div className="hourly-chart">
                  <h5>Temperature (°C)</h5>
                  
                  <div className="chart-container-with-labels">
                    <div className="line-chart-container">
                      <svg className="line-chart" viewBox="0 0 1000 200" preserveAspectRatio="none">
                        {/* Line path */}
                        <path
                          className="temperature-line"
                          d={(() => {
                            const points = weather.hourly_temperature.slice(0, 24).map((temp, idx) => {
                              const x = (idx / 23) * 1000;
                              const y = 200 - ((temp - weather.low) / (weather.high - weather.low)) * 200;
                              return `${idx === 0 ? 'M' : 'L'} ${x} ${y}`;
                            }).join(' ');
                            return points;
                          })()}
                          fill="none"
                        />
                        
                        {/* Area fill */}
                        <path
                          className="temperature-area"
                          d={(() => {
                            const points = weather.hourly_temperature.slice(0, 24).map((temp, idx) => {
                              const x = (idx / 23) * 1000;
                              const y = 200 - ((temp - weather.low) / (weather.high - weather.low)) * 200;
                              return `${idx === 0 ? 'M' : 'L'} ${x} ${y}`;
                            }).join(' ');
                            return points + ' L 1000 200 L 0 200 Z';
                          })()}
                        />
                      </svg>
                      
                      {/* Temperature dots and labels */}
                      {weather.hourly_temperature.slice(0, 24).map((temp, idx) => {
                        const x = (idx / 23) * 1000;
                        const y = 200 - ((temp - weather.low) / (weather.high - weather.low)) * 200;
                        return (
                          <div
                            key={idx}
                            className="data-point"
                            style={{
                              left: `${(idx / 23) * 100}%`,
                              top: `${100 - ((temp - weather.low) / (weather.high - weather.low)) * 100}%`
                            }}
                          >
                            <div className="temp-dot"></div>
                            <div className="temp-label">{temp?.toFixed(1)}°</div>
                            <div className="tooltip">
                              <div className="tooltip-header">
                                {weather.hourly_times && weather.hourly_times[idx] ? 
                                  new Date(weather.hourly_times[idx]).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }) 
                                  : `Hour ${idx + 1}`}
                              </div>
                              <div className="tooltip-row">
                                <span className="tooltip-label">🌡️ Temp:</span>
                                <span>{temp?.toFixed(1)}°C</span>
                              </div>
                              <div className="tooltip-row">
                                <span className="tooltip-label">💧 Humidity:</span>
                                <span>{weather.hourly_humidity?.[idx]?.toFixed(0)}%</span>
                              </div>
                              <div className="tooltip-row">
                                <span className="tooltip-label">🌧️ Precip:</span>
                                <span>{weather.hourly_precipitation?.[idx]?.toFixed(1)} mm</span>
                              </div>
                              <div className="tooltip-row">
                                <span className="tooltip-label">💨 Wind:</span>
                                <span>{weather.hourly_wind?.[idx]?.toFixed(1)} km/h</span>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                    
                    <div className="x-axis">
                      {weather.hourly_times && weather.hourly_times.slice(0, 24).map((time, idx) => {
                        if (idx % 3 === 0) {
                          return (
                            <div key={idx} className="x-axis-label">
                              {new Date(time).toLocaleTimeString('en-US', { hour: '2-digit' })}
                            </div>
                          );
                        }
                        return <div key={idx} className="x-axis-label empty"></div>;
                      })}
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="hourly-stats">
                <div className="stat-item">
                  <span className="label">Avg Humidity:</span>
                  <span className="value">
                    {(weather.hourly_humidity?.reduce((a, b) => a + b, 0) / weather.hourly_humidity?.length || 0).toFixed(0)}%
                  </span>
                </div>
                <div className="stat-item">
                  <span className="label">Total Precip:</span>
                  <span className="value">
                    {(weather.hourly_precipitation?.reduce((a, b) => a + b, 0) || 0).toFixed(1)} mm
                  </span>
                </div>
                <div className="stat-item">
                  <span className="label">Max Wind:</span>
                  <span className="value">
                    {(Math.max(...weather.hourly_wind || [0]) || 0).toFixed(1)} km/h
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
      
      {weather && (
        <LocationIntegrations location={weather.location} />
      )}
    </div>
  );
}

export default CurrentWeather;
