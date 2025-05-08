'''Database manager for handling all database operations.'''
import sqlite3
from contextlib import contextmanager
from typing import Optional, Dict, Any, List
import logging
from src.config.settings import DB_CONFIG

logger = logging.getLogger(__name__)

class DatabaseManager:
    '''Manages database connections and operations.'''
    
    def __init__(self):
        '''Initialize the database manager.'''
        self._init_db()
    
    @contextmanager
    def get_connection(self):
        '''Get a database connection with proper error handling.'''
        conn = None
        try:
            conn = sqlite3.connect(
                DB_CONFIG['path'],
                timeout=DB_CONFIG['timeout']
            )
            yield conn
        except sqlite3.Error as e:
            logger.error(f'Database error: {e}')
            raise
        finally:
            if conn:
                conn.close()
    
    def _init_db(self):
        '''Initialize the database with required tables.'''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    handle TEXT NOT NULL,
                    verified INTEGER NOT NULL DEFAULT 0,
                    verification_code TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM users WHERE user_id = ?',
                    (user_id,)
                )
                row = cursor.fetchone()
                if row:
                    return {
                        'user_id': row[0],
                        'name': row[1],
                        'handle': row[2],
                        'verified': bool(row[3]),
                        'verification_code': row[4],
                        'created_at': row[5],
                        'updated_at': row[6]
                    }
                return None
        except sqlite3.Error as e:
            logger.error(f'Error getting user data: {e}')
            return None
    
    def add_user(self, user_id: int, name: str, handle: str, verification_code: str) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    INSERT INTO users 
                    (user_id, name, handle, verified, verification_code)
                    VALUES (?, ?, ?, ?, ?)
                    ''',
                    (user_id, name, handle, False, verification_code)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            logger.error(f'Error adding user: {e}')
            return False
    
    def update_user_verification(self, user_id: int, verified: bool) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    UPDATE users 
                    SET verified = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                    ''',
                    (verified, user_id)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            logger.error(f'Error updating user verification: {e}')
            return False
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users')
                rows = cursor.fetchall()
                return [{
                    'user_id': row[0],
                    'name': row[1],
                    'handle': row[2],
                    'verified': bool(row[3]),
                    'verification_code': row[4],
                    'created_at': row[5],
                    'updated_at': row[6]
                } for row in rows]
        except sqlite3.Error as e:
            logger.error(f'Error getting all users: {e}')
            return []
    
    def reset_user(self, user_id: int) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'DELETE FROM users WHERE user_id = ?',
                    (user_id,)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            logger.error(f'Error resetting user: {e}')
            return False

# Create a singleton instance
db = DatabaseManager() 