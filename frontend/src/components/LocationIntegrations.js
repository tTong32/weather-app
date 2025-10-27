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

  // Load integrations automatically when location changes
  useEffect(() => {
    if (location && !loading) {
      // Clear previous integrations and load new ones
      setIntegrations(null);
      setError(null);
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
        {loading ? 'Loading...' : (isExpanded ? '▼ Related Videos' : '▶ Related Videos')}
      </button>
      
      {error && <div className="error">{error}</div>}
      
      {isExpanded && (integrations || loading) && (
        <div className="integrations-content">
          {loading && !integrations && <p>Loading related videos...</p>}
          
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
