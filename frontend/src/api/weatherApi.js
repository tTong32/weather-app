import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Current weather
export const getCurrentWeather = async (location) => {
  const response = await api.get(`/api/weather/current?location=${location}`);
  return response.data;
};

// 5-day forecast
export const getForecast = async (location) => {
  const response = await api.get(`/api/weather/forecast?location=${location}`);
  return response.data;
};

// History CRUD operations
export const getAllWeatherRecords = async () => {
  const response = await api.get('/api/weather/history');
  return response.data;
};

export const createWeatherRecord = async (location, startDate, endDate) => {
  const response = await api.post('/api/weather/history', {
    location,
    start_date: startDate,
    end_date: endDate,
  });
  return response.data;
};

export const updateWeatherRecord = async (recordId, location, startDate, endDate) => {
  const response = await api.put(`/api/weather/history/${recordId}`, {
    location,
    start_date: startDate,
    end_date: endDate,
  });
  return response.data;
};

export const deleteWeatherRecord = async (recordId) => {
  const response = await api.delete(`/api/weather/history/${recordId}`);
  return response.data;
};

// Export functions
export const exportWeatherRecordsJSON = async () => {
  const response = await api.get('/api/weather/export/json', {
    responseType: 'blob'
  });
  return response.data;
};

export const exportWeatherRecordsCSV = async () => {
  const response = await api.get('/api/weather/export/csv', {
    responseType: 'blob'
  });
  return response.data;
};

export const exportWeatherRecordsMarkdown = async () => {
  const response = await api.get('/api/weather/export/markdown', {
    responseType: 'blob'
  });
  return response.data;
};

export const exportWeatherRecordJSON = async (recordId) => {
  const response = await api.get(`/api/weather/export/record/${recordId}/json`, {
    responseType: 'blob'
  });
  return response.data;
};

export const exportWeatherRecordCSV = async (recordId) => {
  const response = await api.get(`/api/weather/export/record/${recordId}/csv`, {
    responseType: 'blob'
  });
  return response.data;
};

// Additional API integrations
export const getLocationVideos = async (location, maxResults = 5) => {
  const response = await api.get(`/api/location/videos?location=${encodeURIComponent(location)}&max_results=${maxResults}`);
  return response.data;
};


export const getLocationIntegrations = async (location) => {
  const response = await api.get(`/api/location/integrations?location=${encodeURIComponent(location)}`);
  return response.data;
};

// Location search functions
export const searchLocations = async (query, limit = 5) => {
  const response = await api.get(`/api/location/search?query=${encodeURIComponent(query)}&limit=${limit}`);
  return response.data;
};

export const getLocationDetails = async (latitude, longitude) => {
  const response = await api.get(`/api/location/details?latitude=${latitude}&longitude=${longitude}`);
  return response.data;
};

export default api;
