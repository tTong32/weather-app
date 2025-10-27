from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
import json
import csv
import io
from datetime import datetime
from typing import Optional

from app.repository import weather_repo

router = APIRouter()

@router.get("/export/json", summary="Export weather records as JSON")
def export_json():
    """Export all weather records as JSON file"""
    try:
        records = weather_repo.read_all_records()
        
        # Convert weather_json strings back to objects for better readability
        for record in records:
            if record.get('weather_json'):
                try:
                    record['weather_data'] = json.loads(record['weather_json'])
                except json.JSONDecodeError:
                    record['weather_data'] = record['weather_json']
        
        # Create JSON response
        json_data = json.dumps(records, indent=2, default=str)
        
        # Create file-like object
        json_file = io.StringIO(json_data)
        
        return StreamingResponse(
            io.BytesIO(json_file.getvalue().encode('utf-8')),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=weather_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export JSON: {str(e)}")

@router.get("/export/csv", summary="Export weather records as CSV")
def export_csv():
    """Export all weather records as CSV file with actual weather data"""
    try:
        records = weather_repo.read_all_records()
        
        if not records:
            raise HTTPException(status_code=404, detail="No records found to export")
        
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header for weather data
        writer.writerow(['Date', 'Time', 'Temperature (°C)', 'Precipitation (mm)', 'Wind Speed (m/s)', 'Location'])
        
        # Process each record and extract weather data
        for record in records:
            if not record.get('weather_json'):
                continue
                
            try:
                weather_data = json.loads(record['weather_json'])
                location = record.get('location', '')
                
                # Extract hourly data arrays
                times = weather_data.get('hourly', {}).get('time', [])
                temperatures = weather_data.get('hourly', {}).get('temperature_2m', [])
                precipitations = weather_data.get('hourly', {}).get('precipitation', [])
                wind_speeds = weather_data.get('hourly', {}).get('wind_speed_10m', [])
                
                # Write each hourly data point as a row
                for i, time_str in enumerate(times):
                    # Parse datetime string (format: 2023-01-01T00:00)
                    dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                    date_str = dt.strftime('%Y-%m-%d')
                    time_str_formatted = dt.strftime('%H:%M')
                    
                    # Get corresponding values (handle missing data gracefully)
                    temp = temperatures[i] if i < len(temperatures) else ''
                    precip = precipitations[i] if i < len(precipitations) else ''
                    wind = wind_speeds[i] if i < len(wind_speeds) else ''
                    
                    writer.writerow([
                        date_str,
                        time_str_formatted,
                        temp,
                        precip,
                        wind,
                        location
                    ])
                    
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                # Skip records with invalid weather data
                continue
        
        # Create file-like object
        csv_content = output.getvalue()
        
        return StreamingResponse(
            io.BytesIO(csv_content.encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export CSV: {str(e)}")

@router.get("/export/markdown", summary="Export weather records as Markdown")
def export_markdown():
    """Export all weather records as Markdown file"""
    try:
        records = weather_repo.read_all_records()
        
        if not records:
            raise HTTPException(status_code=404, detail="No records found to export")
        
        # Create Markdown content
        markdown_content = f"""# Weather Records Export
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Records: {len(records)}

## Records Summary

| ID | Location | Start Date | End Date | Created At |
|---|---|---|---|---|
"""
        
        for record in records:
            markdown_content += f"| {record.get('id', '')} | {record.get('location', '')} | {record.get('start_date', '')} | {record.get('end_date', '')} | {record.get('created_at', '')} |\n"
        
        markdown_content += "\n## Detailed Records\n\n"
        
        for record in records:
            markdown_content += f"""### Record {record.get('id', '')}: {record.get('location', '')}
- **Location**: {record.get('location', '')}
- **Date Range**: {record.get('start_date', '')} to {record.get('end_date', '')}
- **Created**: {record.get('created_at', '')}
- **Weather Data**: {'Available' if record.get('weather_json') else 'Not available'}

"""
        
        return StreamingResponse(
            io.BytesIO(markdown_content.encode('utf-8')),
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename=weather_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export Markdown: {str(e)}")

@router.get("/export/record/{record_id}/csv", summary="Export specific weather record as CSV")
def export_record_csv(record_id: int):
    """Export a specific weather record as CSV file with actual weather data"""
    try:
        record = weather_repo.return_record(record_id)
        
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        
        if not record.get('weather_json'):
            raise HTTPException(status_code=404, detail="No weather data available for this record")
        
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header for weather data
        writer.writerow(['Date', 'Time', 'Temperature (°C)', 'Precipitation (mm)', 'Wind Speed (m/s)', 'Location'])
        
        try:
            weather_data = json.loads(record['weather_json'])
            location = record.get('location', '')
            
            # Extract hourly data arrays
            times = weather_data.get('hourly', {}).get('time', [])
            temperatures = weather_data.get('hourly', {}).get('temperature_2m', [])
            precipitations = weather_data.get('hourly', {}).get('precipitation', [])
            wind_speeds = weather_data.get('hourly', {}).get('wind_speed_10m', [])
            
            # Write each hourly data point as a row
            for i, time_str in enumerate(times):
                # Parse datetime string (format: 2023-01-01T00:00)
                dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                date_str = dt.strftime('%Y-%m-%d')
                time_str_formatted = dt.strftime('%H:%M')
                
                # Get corresponding values (handle missing data gracefully)
                temp = temperatures[i] if i < len(temperatures) else ''
                precip = precipitations[i] if i < len(precipitations) else ''
                wind = wind_speeds[i] if i < len(wind_speeds) else ''
                
                writer.writerow([
                    date_str,
                    time_str_formatted,
                    temp,
                    precip,
                    wind,
                    location
                ])
                
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse weather data: {str(e)}")
        
        # Create file-like object
        csv_content = output.getvalue()
        
        return StreamingResponse(
            io.BytesIO(csv_content.encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=weather_record_{record_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export record CSV: {str(e)}")
