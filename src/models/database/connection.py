import sqlite3
from contextlib import contextmanager
import logging
from src.config.settings import DB_CONFIG

logger = logging.getLogger(__name__)

class ConnectionManager:
    @staticmethod
    @contextmanager
    def get_connection():
        conn = None
        try:
            conn = sqlite3.connect(
                DB_CONFIG['path'],
                timeout = DB_CONFIG['timeout']
            )
            yield conn
        except sqlite3.Error as e:
            logger.error(f'Database error: {e}')
            raise
        finally:
            if conn:
                conn.close()