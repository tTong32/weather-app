import requests
import os
from typing import Optional, Dict, Any

class AdditionalAPIService:
    """Service for integrating Youtube API"""
    
    def __init__(self):
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY', '')
    
    def get_location_videos(self, location: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Get YouTube videos related to a location
        """
        if not self.youtube_api_key:
            return {
                "error": "YouTube API key not configured",
                "videos": [],
                "message": "YouTube integration requires API key setup"
            }
        
        try:
            # Create more specific search queries for better location relevance
            location_parts = location.split(',')
            city_name = location_parts[0].strip()
            
            # Check if the location is coordinates (starts with a number)
            if city_name.replace('.', '').replace('-', '').isdigit():
                # If it's coordinates, try to get city name from reverse geocoding
                try:
                    from app.services.location_search import get_location_details
                    lat, lon = float(city_name), float(location_parts[1].strip())
                    location_details = get_location_details(lat, lon)
                    if location_details and location_details.get('name'):
                        city_name = location_details['name']
                        search_query = f'"{city_name}" city guide attractions'
                    else:
                        # Fallback to generic search
                        search_query = f"travel guide attractions"
                except:
                    # Fallback to generic search
                    search_query = f"travel guide attractions"
            else:
                # If it's a city name, use specific search
                search_queries = [
                    f'"{city_name}" city guide attractions',
                    f'"{city_name}" things to do places to visit',
                    f'"{city_name}" travel guide tourism',
                    f'"{city_name}" landmarks attractions'
                ]
                search_query = search_queries[0]
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'q': search_query,
                'type': 'video',
                'maxResults': max_results,
                'key': self.youtube_api_key,
                'order': 'relevance'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            videos = []
            for item in data.get('items', []):
                video = {
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'][:200] + '...' if len(item['snippet']['description']) > 200 else item['snippet']['description'],
                    'thumbnail': item['snippet']['thumbnails'].get('medium', {}).get('url', ''),
                    'video_id': item['id']['videoId'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'channel': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt']
                }
                videos.append(video)
            
            return {
                "success": True,
                "location": location,
                "videos": videos,
                "total_results": len(videos)
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "error": f"YouTube API request failed: {str(e)}",
                "videos": [],
                "message": "Failed to fetch YouTube videos"
            }
        except Exception as e:
            return {
                "error": f"YouTube integration error: {str(e)}",
                "videos": [],
                "message": "Unexpected error occurred"
            }

# Create a global instance
additional_api_service = AdditionalAPIService()
