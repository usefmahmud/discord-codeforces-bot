'''Codeforces API client for handling all API interactions.'''
import time
import logging
from typing import Optional, Dict, Any
import requests
from src.config.settings import CODEFORCES_API

logger = logging.getLogger(__name__)

class CodeforcesClient:
    
    def __init__(self):
        self.base_url = CODEFORCES_API['base_url']
        self.rate_limit = CODEFORCES_API['rate_limit']
        self.last_request = 0
    
    def _wait_for_rate_limit(self):
        current_time = time.time()
        time_since_last = current_time - self.last_request
        if time_since_last < self.rate_limit:
            time.sleep(self.rate_limit - time_since_last)
        self.last_request = time.time()
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        try:
            self._wait_for_rate_limit()
            url = f'{self.base_url}/{endpoint}'
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] != 'OK':
                logger.error(f'Codeforces API error: {data.get("comment", "Unknown error")}')
                return None
                
            return data['result']
        except requests.RequestException as e:
            logger.error(f'Error making request to Codeforces API: {e}')
            return None
    
    def get_user_info(self, handle: str) -> Optional[Dict[str, Any]]:
        result = self._make_request('user.info', {'handles': handle})
        if result and isinstance(result, list) and len(result) > 0:
            return result[0]
        return None
    
    def get_user_rating(self, handle: str) -> Optional[Dict[str, Any]]:
        return self._make_request('user.rating', {'handle': handle})
    
    def get_user_submissions(self, handle: str, count: int = 10) -> Optional[Dict[str, Any]]:
        return self._make_request('user.status', {
            'handle': handle,
            'count': count
        })
    
    def get_user_rating_colour(self, rank: str) -> Optional[int]:
        cf_ratings = {
            'newbie': 0x808080,
            'pupil': 0x77dd77,
            'specialist': 0x74b9ff,
            'expert': 0xa29bff,
            'candidate master': 0xfeca57,
            'master': 0xff6b6b,
            'international master': 0xffb86c,
            'grandmaster': 0xfb355d,
            'international grandmaster': 0xebb424
        }
        return cf_ratings.get(rank.lower(), 0x808080)
                

# Create a singleton instance
cf_client = CodeforcesClient() 