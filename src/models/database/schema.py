import logging
from src.models.database.connection import ConnectionManager
from src.models.user import UserManager

logger = logging.getLogger(__name__)

def initialize_schema():
    try:
        with ConnectionManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    handle TEXT NOT NULL,
                    verified INTEGER NOT NULL DEFAULT 0,
                    verification_code TEXT NOT NULL,
                    rank TEXT DEFAULT 'unrated',
                    rating INTEGER DEFAULT 0,
                    points INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            logger.info("Database schema initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database schema: {e}")
        raise
    
