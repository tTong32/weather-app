import React, { useState } from 'react';
import './Header.css';

function Header() {
  const [showInfo, setShowInfo] = useState(false);

  return (
    <header className="header">
      <div className="header-content">
        <h1>Weather App</h1>
        <div className="header-info">
          <p>by Thomson Tong</p>
          <button 
            className="info-btn" 
            onClick={() => setShowInfo(!showInfo)}
            aria-label="Show info"
          >
            ℹ️
          </button>
        </div>
      </div>
      
      {showInfo && (
        <div className="info-modal">
          <h3>Product Manager Accelerator</h3>
          <p>
            This weather app was built for the Product Manager Accelerator program.
            Connect with us on 
            <a 
              href="https://www.linkedin.com/company/product-manager-accelerator" 
              target="_blank" 
              rel="noopener noreferrer"
            >
              {' '}LinkedIn
            </a>
          </p>
          <button onClick={() => setShowInfo(false)} className="close-btn">
            Close
          </button>
        </div>
      )}
    </header>
  );
}

export default Header;
