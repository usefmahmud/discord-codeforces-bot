'''Configuration settings for the bot.'''
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
DB_PATH = DATA_DIR / 'bot.db'

DATA_DIR.mkdir(exist_ok=True)


BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError('BOT_TOKEN environment variable is not set')


DB_CONFIG: Dict[str, Any] = {
    'path': str(DB_PATH),
    'timeout': 30.0,
}

# API settings
CODEFORCES_API = {
    'base_url': 'https://codeforces.com/api',
    'rate_limit': 1.0,  # seconds between requests
}


COMMAND_PREFIX = '/'