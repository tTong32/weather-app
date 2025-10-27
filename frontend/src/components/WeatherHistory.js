import React, { useState, useEffect } from 'react';
import { 
  getAllWeatherRecords, 
  createWeatherRecord, 
  updateWeatherRecord, 
  deleteWeatherRecord,
  exportWeatherRecordsJSON,
  exportWeatherRecordsCSV,
  exportWeatherRecordsMarkdown,
  exportWeatherRecordJSON,
  exportWeatherRecordCSV
} from '../api/weatherApi';
import LocationSearchBar from './LocationSearchBar';
import './WeatherHistory.css';

function WeatherHistory() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingRecord, setEditingRecord] = useState(null);
  const [formData, setFormData] = useState({
    location: '',
    start_date: '',
    end_date: ''
  });

  const handleLocationSelect = (selectedLocation) => {
    setFormData({...formData, location: selectedLocation});
  };

  useEffect(() => {
    loadRecords();
  }, []);

  const loadRecords = async () => {
    try {
      setLoading(true);
      const response = await getAllWeatherRecords();
      setRecords(response.data);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to load records';
      setError(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      
      // Ensure we have valid form data
      if (!formData.location || !formData.start_date || !formData.end_date) {
        setError('Please fill in all fields');
        return;
      }
      
      if (editingRecord) {
        await updateWeatherRecord(editingRecord.id, formData.location, formData.start_date, formData.end_date);
      } else {
        await createWeatherRecord(formData.location, formData.start_date, formData.end_date);
      }
      
      await loadRecords();
      resetForm();
    } catch (err) {
      console.error('Form submission error:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to save record';
      setError(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (record) => {
    setEditingRecord(record);
    setFormData({
      location: record.location,
      start_date: record.start_date,
      end_date: record.end_date
    });
    setShowForm(true);
  };

  const handleDelete = async (recordId) => {
    if (window.confirm('Are you sure you want to delete this record?')) {
      try {
        setLoading(true);
        await deleteWeatherRecord(recordId);
        await loadRecords();
      } catch (err) {
        const errorMessage = err.response?.data?.detail || err.message || 'Failed to delete record';
        setError(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
      } finally {
        setLoading(false);
      }
    }
  };

  const resetForm = () => {
    setFormData({ location: '', start_date: '', end_date: '' });
    setEditingRecord(null);
    setShowForm(false);
  };

  const downloadFile = (blob, filename) => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  const handleExport = async (format) => {
    try {
      setLoading(true);
      let blob, filename;
      
      switch (format) {
        case 'json':
          blob = await exportWeatherRecordsJSON();
          filename = `weather_records_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
          break;
        case 'csv':
          blob = await exportWeatherRecordsCSV();
          filename = `weather_records_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.csv`;
          break;
        case 'markdown':
          blob = await exportWeatherRecordsMarkdown();
          filename = `weather_records_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.md`;
          break;
        default:
          throw new Error('Invalid export format');
      }
      
      downloadFile(blob, filename);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to export data';
      setError(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
    } finally {
      setLoading(false);
    }
  };

  const handleExportRecord = async (recordId) => {
    try {
      setLoading(true);
      const blob = await exportWeatherRecordJSON(recordId);
      const filename = `weather_record_${recordId}_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
      downloadFile(blob, filename);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to export record';
      setError(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
    } finally {
      setLoading(false);
    }
  };

  const handleExportRecordCSV = async (record) => {
    try {
      setLoading(true);
      
      const blob = await exportWeatherRecordCSV(record.id);
      const filename = `weather_record_${record.id}_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.csv`;
      downloadFile(blob, filename);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to export record';
      setError(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
    } finally {
      setLoading(false);
    }
  };

  const handleExportRecordMarkdown = async (record) => {
    try {
      setLoading(true);
      
      // Create Markdown content for single record
      const markdownContent = `# Weather Record ${record.id}

## Record Details
- **Location**: ${record.location}
- **Date Range**: ${record.start_date} to ${record.end_date}
- **Created**: ${record.created_at}
- **Weather Data**: ${record.weather_json ? 'Available' : 'Not available'}

## Export Information
- **Exported on**: ${new Date().toLocaleString()}
- **Record ID**: ${record.id}
`;
      
      const blob = new Blob([markdownContent], { type: 'text/markdown' });
      const filename = `weather_record_${record.id}_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.md`;
      downloadFile(blob, filename);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to export record';
      setError(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="weather-history">
      <div className="history-header">
        <h2>Weather History Management</h2>
        <div className="history-actions">
          <button 
            className="btn btn-primary" 
            onClick={() => setShowForm(true)}
            disabled={loading}
          >
            ➕ Add Record
          </button>
        </div>
      </div>

      {showForm && (
        <div className="form-modal">
          <div className="form-content">
            <div className="form-header">
              <h3>{editingRecord ? 'Edit Record' : 'Add New Record'}</h3>
              <button className="close-btn" onClick={resetForm}>✕</button>
            </div>
            
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Location:</label>
                <LocationSearchBar 
                  onLocationSelect={handleLocationSelect}
                  placeholder="Search for a location..."
                />
                {formData.location && (
                  <div className="selected-location">
                    <small>Selected: {formData.location}</small>
                  </div>
                )}
              </div>
              
              <div className="form-group">
                <label>Start Date:</label>
                <input
                  type="date"
                  value={formData.start_date}
                  onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>End Date:</label>
                <input
                  type="date"
                  value={formData.end_date}
                  onChange={(e) => setFormData({...formData, end_date: e.target.value})}
                  required
                />
              </div>
              
              <div className="form-actions">
                <button type="submit" className="btn btn-primary" disabled={loading}>
                  {loading ? 'Saving...' : (editingRecord ? 'Update' : 'Create')}
                </button>
                <button type="button" className="btn btn-secondary" onClick={resetForm}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">{error}</div>}

      <div className="records-grid">
        {records.map((record) => (
          <div key={record.id} className="record-card">
            <div className="record-header">
              <h4>{record.location}</h4>
              <div className="record-actions">
                <button 
                  className="btn btn-small btn-edit" 
                  onClick={() => handleEdit(record)}
                  title="Edit this record"
                >
                  ✏️
                </button>
                <button 
                  className="btn btn-small btn-delete" 
                  onClick={() => handleDelete(record.id)}
                  title="Delete this record"
                >
                  🗑️
                </button>
              </div>
            </div>
            
            <div className="record-details">
              <div className="detail-item">
                <span className="label">Date Range:</span>
                <span>{record.start_date} to {record.end_date}</span>
              </div>
              <div className="detail-item">
                <span className="label">Created:</span>
                <span>{new Date(record.created_at).toLocaleDateString()}</span>
              </div>
              <div className="detail-item">
                <span className="label">Weather Data:</span>
                <span>{record.weather_json ? '✅ Available' : '❌ Not available'}</span>
              </div>
            </div>
            
            <div className="record-export-section">
              <div className="export-label">Export Options:</div>
              <div className="export-buttons">
                <button 
                  className="btn btn-small btn-export" 
                  onClick={() => handleExportRecord(record.id)}
                  title="Export as JSON"
                >
                  📄 JSON
                </button>
                <button 
                  className="btn btn-small btn-export" 
                  onClick={() => handleExportRecordCSV(record)}
                  title="Export as CSV"
                >
                  📊 CSV
                </button>
                <button 
                  className="btn btn-small btn-export" 
                  onClick={() => handleExportRecordMarkdown(record)}
                  title="Export as Markdown"
                >
                  📝 MD
                </button>
              </div>
            </div>
          </div>
        ))}
        
        {records.length === 0 && !loading && (
          <div className="no-records">
            <p>No weather records found. Create your first record to get started!</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default WeatherHistory;
