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

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS problems (
                    problem_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contest_id INTEGER NOT NULL,
                    problem_index TEXT NOT NULL,
                    problem_name TEXT NOT NULL,
                    problem_rating INTEGER DEFAULT 0,
                    problem_link TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tags (
                    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag_name TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS problem_tags (
                    problem_id INTEGER NOT NULL,
                    tag_id INTEGER NOT NULL,
                    PRIMARY KEY (problem_id, tag_id),
                    FOREIGN KEY (problem_id) REFERENCES problems(problem_id),
                    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
                )
            ''')

            conn.commit()
            logger.info("Database schema initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database schema: {e}")
        raise
    
