'''Database manager for handling all database operations.'''
import sqlite3
from contextlib import contextmanager
from typing import Optional, Dict, Any, List
import logging
from src.models.database.connection import ConnectionManager

logger = logging.getLogger(__name__)

class UserManager:
    @staticmethod
    def get(user_id: int) -> Optional[Dict[str, Any]]:
        try:
            with ConnectionManager.get_connection() as conn:
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
                        'rank': row[5],
                        'rating': row[6],
                        'created_at': row[7],
                        'updated_at': row[8]
                    }
                return None
        except sqlite3.Error as e:
            logger.error(f'Error getting user data: {e}')
            return None
        
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        try:
            with ConnectionManager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users')
                rows = cursor.fetchall()
                return [{
                    'user_id': row[0],
                    'name': row[1],
                    'handle': row[2],
                    'verified': bool(row[3]),
                    'verification_code': row[4],
                    'rank': row[5],
                    'rating': row[6],
                    'points': row[7],
                    'created_at': row[8],
                    'updated_at': row[9]
                } for row in rows]
        except sqlite3.Error as e:
            logger.error(f'Error getting all users: {e}')
            return []
    
    def add_user(self, user_id: int, name: str, handle: str, verification_code: str) -> bool:
        try:
            with ConnectionManager.get_connection() as conn:
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
        
    def update_user(self, user_id: int, **kwargs: Optional[Dict[str, Any]]) -> bool:
        try:
            if not kwargs:
                return False
                
            update_fields = []
            values = []
            
            for field, value in kwargs.items():
                if field in ['name', 'handle', 'verified', 'rank', 'rating', 'points']:
                    update_fields.append(f"{field} = ?")
                    values.append(value)
            
            if not update_fields:
                return False
                
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            values.append(user_id)
            
            with ConnectionManager.get_connection() as conn:
                cursor = conn.cursor()
                query = f'''
                    UPDATE users 
                    SET {', '.join(update_fields)}
                    WHERE user_id = ?
                '''
                cursor.execute(query, values)
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            logger.error(f'Error updating user: {e}')
            return False
    
    
    
    def reset_user(self, user_id: int) -> bool:
        try:
            with ConnectionManager.get_connection() as conn:
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
        
    @staticmethod
    def get_by_rating() -> List[Dict[str, Any]]:
        try:
            with ConnectionManager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users ORDER BY rating DESC LIMIT 10')
                rows = cursor.fetchall()
                return [{
                    'user_id': row[0],
                    'name': row[1],
                    'handle': row[2],
                    'rank': row[5],
                    'rating': row[6],
                    'points': row[7]
                } for row in rows]
        except sqlite3.Error as e:
            logger.error(f'Error getting leaderboard by rating: {e}')
            return []
        
    @staticmethod
    def get_by_points() -> List[Dict[str, Any]]:
        try:
            with ConnectionManager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users ORDER BY points DESC LIMIT 10')
                rows = cursor.fetchall()
                return [{
                    'user_id': row[0],
                    'name': row[1],
                    'handle': row[2],
                    'rank': row[5],
                    'rating': row[6],
                    'points': row[7]
                } for row in rows]
        except sqlite3.Error as e:
            logger.error(f'Error getting leaderboard by points: {e}')
            return []
                
    @staticmethod
    def is_handle_exists(handle: str) -> bool:
        try:
            with ConnectionManager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM users WHERE handle = ?', (handle,))
                return cursor.fetchone()[0] > 0
        except sqlite3.Error as e:
            logger.error(f'Error checking if handle exists: {e}')
            return False


# Create a singleton instance
UserManager = UserManager() 