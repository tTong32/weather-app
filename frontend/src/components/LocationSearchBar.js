import React, { useState, useEffect, useRef } from 'react';
import { searchLocations } from '../api/weatherApi';
import './LocationSearchBar.css';

function LocationSearchBar({ onLocationSelect, placeholder = "Search for a location..." }) {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const [error, setError] = useState(null);
  const [isSelecting, setIsSelecting] = useState(false);
  
  const searchTimeoutRef = useRef(null);
  const inputRef = useRef(null);
  const suggestionsRef = useRef(null);

  // Debounced search function
  useEffect(() => {
    if (query.length < 2 || isSelecting) {
      setSuggestions([]);
      setShowSuggestions(false);
      setError(null); // Clear error when not searching
      return;
    }

    // Clear previous timeout
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    // Set new timeout for search
    searchTimeoutRef.current = setTimeout(async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        const response = await searchLocations(query, 8);
        setSuggestions(response.data.locations);
        setShowSuggestions(true);
        setSelectedIndex(-1);
      } catch (err) {
        setError('Failed to search locations');
        setSuggestions([]);
        setShowSuggestions(false);
      } finally {
        setIsLoading(false);
      }
    }, 300); // 300ms delay

    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, [query, isSelecting]);

  // Handle input change
  const handleInputChange = (e) => {
    setQuery(e.target.value);
    setError(null);
    setIsSelecting(false); // Reset selecting flag when user types
  };

  // Handle suggestion selection
  const handleSuggestionSelect = (suggestion) => {
    setIsSelecting(true); // Prevent search from running
    setQuery(suggestion.display_name);
    setShowSuggestions(false);
    setSuggestions([]);
    setError(null); // Clear any existing errors
    onLocationSelect(suggestion.search_query);
    
    // Reset selecting flag after a longer delay to prevent search from running
    setTimeout(() => {
      setIsSelecting(false);
    }, 500);
  };

  // Handle keyboard navigation
  const handleKeyDown = (e) => {
    if (!showSuggestions || suggestions.length === 0) {
      if (e.key === 'Enter') {
        // If no suggestions, try to use the query as-is
        onLocationSelect(query);
        setShowSuggestions(false);
      }
      return;
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => 
          prev < suggestions.length - 1 ? prev + 1 : prev
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => prev > 0 ? prev - 1 : -1);
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0 && selectedIndex < suggestions.length) {
          handleSuggestionSelect(suggestions[selectedIndex]);
        } else {
          onLocationSelect(query);
          setShowSuggestions(false);
        }
        break;
      case 'Escape':
        setShowSuggestions(false);
        setSelectedIndex(-1);
        break;
    }
  };

  // Handle click outside to close suggestions
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        suggestionsRef.current && 
        !suggestionsRef.current.contains(event.target) &&
        inputRef.current &&
        !inputRef.current.contains(event.target)
      ) {
        setShowSuggestions(false);
        setSelectedIndex(-1);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Clear suggestions when input is cleared
  useEffect(() => {
    if (query === '') {
      setSuggestions([]);
      setShowSuggestions(false);
      setSelectedIndex(-1);
    }
  }, [query]);

  return (
    <div className="location-search-container">
      <div className="search-input-wrapper">
        <div className="search-icon">🔍</div>
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onFocus={() => {
            if (suggestions.length > 0) {
              setShowSuggestions(true);
            }
          }}
          placeholder={placeholder}
          className="location-search-input"
          autoComplete="off"
        />
        {isLoading && <div className="loading-spinner">⏳</div>}
        {query && (
          <button
            className="clear-button"
            onClick={() => {
              setQuery('');
              setShowSuggestions(false);
              setSuggestions([]);
              setError(null);
              setIsSelecting(false);
              inputRef.current?.focus();
            }}
            type="button"
          >
            ✕
          </button>
        )}
      </div>

      {error && (
        <div className="search-error">
          {error}
        </div>
      )}

      {showSuggestions && suggestions.length > 0 && (
        <div ref={suggestionsRef} className="suggestions-dropdown">
          {suggestions.map((suggestion, index) => (
            <div
              key={`${suggestion.latitude}-${suggestion.longitude}`}
              className={`suggestion-item ${index === selectedIndex ? 'selected' : ''}`}
              onClick={() => handleSuggestionSelect(suggestion)}
              onMouseEnter={() => setSelectedIndex(index)}
            >
              <div className="suggestion-main">
                <div className="suggestion-name">{suggestion.name}</div>
                <div className="suggestion-details">
                  {suggestion.admin1 && suggestion.admin1 !== suggestion.name && (
                    <span className="suggestion-admin">{suggestion.admin1}</span>
                  )}
                  {suggestion.country && (
                    <span className="suggestion-country">{suggestion.country}</span>
                  )}
                </div>
              </div>
              <div className="suggestion-coords">
                {suggestion.latitude.toFixed(4)}, {suggestion.longitude.toFixed(4)}
              </div>
            </div>
          ))}
          
          {suggestions.length === 8 && (
            <div className="suggestion-footer">
              <small>Showing top results. Try a more specific search.</small>
            </div>
          )}
        </div>
      )}

      {showSuggestions && suggestions.length === 0 && query.length >= 2 && !isLoading && (
        <div className="suggestions-dropdown">
          <div className="no-suggestions">
            <div className="no-suggestions-icon">📍</div>
            <div className="no-suggestions-text">
              <div>No locations found for "{query}"</div>
              <small>Try a different search term or check spelling</small>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default LocationSearchBar;
