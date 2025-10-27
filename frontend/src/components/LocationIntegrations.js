import React, { useState, useEffect } from 'react';
import { getLocationIntegrations } from '../api/weatherApi';
import './LocationIntegrations.css';

function LocationIntegrations({ location }) {
  const [integrations, setIntegrations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isExpanded, setIsExpanded] = useState(true);

  const handleLoadIntegrations = async () => {
    if (!location || loading) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await getLocationIntegrations(location);
      setIntegrations(response.data);
      setIsExpanded(true);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load integrations');
    } finally {
      setLoading(false);
    }
  };

  // Load integrations automatically when component mounts
  useEffect(() => {
    if (location && !integrations && !loading) {
      handleLoadIntegrations();
    }
  }, [location]);

  const handleToggleExpanded = () => {
    setIsExpanded(!isExpanded);
  };

  if (!location) return null;

  return (
    <div className="location-integrations">
      <button 
        className="integrations-toggle"
        onClick={handleToggleExpanded}
        disabled={loading}
      >
        {loading ? 'Loading...' : (isExpanded ? '▼ 🔗 Location Info & Media' : '▶ 🔗 Location Info & Media')}
      </button>
      
      {error && <div className="error">{error}</div>}
      
      {isExpanded && (integrations || loading) && (
        <div className="integrations-content">
          {loading && !integrations && <p>Loading location information...</p>}
          
          {/* Google Maps Integration */}
          {integrations && integrations.google_maps && (
            <div className="integration-section">
              <h4>Location Details</h4>
              {integrations.google_maps.success ? (
                <div className="map-info">
                  <div className="map-details">
                    <p><strong>Address:</strong> {integrations.google_maps.map_info.formatted_address}</p>
                    <p><strong>Coordinates:</strong> {integrations.google_maps.map_info.latitude.toFixed(4)}, {integrations.google_maps.map_info.longitude.toFixed(4)}</p>
                    {integrations.google_maps.map_info.place_info.rating > 0 && (
                      <p><strong>Rating:</strong> ⭐ {integrations.google_maps.map_info.place_info.rating}/5 ({integrations.google_maps.map_info.place_info.user_ratings_total} reviews)</p>
                    )}
                  </div>
                  <a 
                    href={integrations.google_maps.map_info.google_maps_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="map-link"
                  >
                    🗺️ View on Google Maps
                  </a>
                </div>
              ) : (
                <p className="api-error">{integrations.google_maps.message}</p>
              )}
            </div>
          )}

          {/* YouTube Integration */}
          {integrations && integrations.youtube && (
            <div className="integration-section">
              <h4>Related Videos</h4>
              {integrations.youtube.success ? (
                <div className="videos-grid">
                  {integrations.youtube.videos.map((video, index) => (
                    <div key={index} className="video-card">
                      <div className="video-thumbnail">
                        <img src={video.thumbnail} alt={video.title} />
                        <div className="video-overlay">
                          <a href={video.url} target="_blank" rel="noopener noreferrer">
                            ▶️
                          </a>
                        </div>
                      </div>
                      <div className="video-info">
                        <h5>{video.title}</h5>
                        <p className="video-channel">{video.channel}</p>
                        <p className="video-description">{video.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="api-error">{integrations.youtube.message}</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default LocationIntegrations;
