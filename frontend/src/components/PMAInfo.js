import React, { useState } from 'react';
import './PMAInfo.css';

function PMAInfo() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="pma-info">
      <button 
        className="pma-info-button" 
        onClick={() => setIsOpen(!isOpen)}
        title="About PM Accelerator"
      >
        ℹ️ About PMA
      </button>
      
      {isOpen && (
        <div className="pma-info-modal">
          <div className="pma-info-content">
            <div className="pma-info-header">
              <h3>Weather App by Thomson</h3>
              <button 
                className="pma-info-close" 
                onClick={() => setIsOpen(false)}
              >
                ✕
              </button>
            </div>
            
            <div className="pma-info-body">
              <div className="pma-section">
                <h4>About Product Manager Accelerator (PMA)</h4>
                <p>
                  The Product Manager Accelerator is a comprehensive program designed to accelerate 
                  your career in product management. We provide hands-on training, mentorship, and 
                  real-world experience to help you become a successful product manager.
                </p>
                <p>
                  Our program focuses on practical skills, industry best practices, and building 
                  a strong foundation in product strategy, user research, data analysis, and 
                  cross-functional collaboration.
                </p>
                <div className="pma-links">
                  <a 
                    href="https://www.linkedin.com/company/product-manager-accelerator" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="pma-link"
                  >
                    🔗 Visit our LinkedIn
                  </a>
                </div>
              </div>
              
              <div className="pma-section">
                <h4>About This Weather App</h4>
                <p>
                  This weather application demonstrates full-stack development skills including:
                </p>
                <ul>
                  <li>Real-time weather data integration using Open-Meteo API</li>
                  <li>Multiple location input formats (city, postal code, coordinates)</li>
                  <li>Current weather with detailed hourly forecasts</li>
                  <li>5-day weather forecast with visual icons</li>
                  <li>GPS location detection</li>
                  <li>CRUD operations with SQLite database</li>
                  <li>Historical weather data storage and retrieval</li>
                  <li>Data validation and error handling</li>
                  <li>Responsive design with modern UI/UX</li>
                </ul>
              </div>
              
              <div className="pma-section">
                <h4>Technical Stack</h4>
                <div className="tech-stack">
                  <div className="tech-item">
                    <strong>Frontend:</strong> React.js, CSS3, Axios
                  </div>
                  <div className="tech-item">
                    <strong>Backend:</strong> FastAPI, Python, SQLite
                  </div>
                  <div className="tech-item">
                    <strong>APIs:</strong> Open-Meteo Weather API, Geocoding API
                  </div>
                  <div className="tech-item">
                    <strong>Features:</strong> Real-time data, CRUD operations, Data persistence
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default PMAInfo;
