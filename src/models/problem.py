import discord 
from src.models.database.connection import ConnectionManager
from src.data.constants import LITERAL_TAGS, LITERAL_RATING
from typing import Optional
import random

class ProblemManager():

    @staticmethod
    def get_random_problem(tag: Optional[LITERAL_TAGS] = None, rating: Optional[LITERAL_RATING] = None) -> Optional[dict]:
        with ConnectionManager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Build the query based on parameters
            if tag:
                query = '''
                    SELECT p.problem_id, p.contest_id, p.problem_index, p.problem_name, p.problem_rating 
                    FROM problems p
                    JOIN problem_tags pt ON p.problem_id = pt.problem_id
                    JOIN tags t ON pt.tag_id = t.tag_id
                    WHERE t.tag_name = ?
                '''
                params = [tag]
                
                if rating:
                    query += ' AND p.problem_rating = ?'
                    params.append(rating)
            else:
                query = 'SELECT * FROM problems'
                params = []
                
                if rating:
                    query += ' WHERE problem_rating = ?'
                    params.append(rating)
            
            query += ' ORDER BY RANDOM() LIMIT 1'
            
            cursor.execute(query, params)
            problem = cursor.fetchone()
            
            if not problem:
                return None
                
            problem_tags = cursor.execute(
                'SELECT tag_name FROM problem_tags JOIN tags ON problem_tags.tag_id = tags.tag_id WHERE problem_id = ?', 
                (problem[0],)
            ).fetchall()
            
            return {
                'problem_id': problem[0],
                'contest_id': problem[1],
                'index': problem[2],
                'name': problem[3],
                'rating': problem[4],
                'tags': [tag[0] for tag in problem_tags],
            }

    @staticmethod
    def add_solved_problem(user_id: int, problem_id: int):
        with ConnectionManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO solved_problems (user_id, problem_id) VALUES (?, ?)', (user_id, problem_id))
            conn.commit()

    @staticmethod
    def get_solved_problems(user_id: int) -> list[dict]:
        with ConnectionManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT p.problem_id, p.contest_id, p.problem_index, p.problem_name, p.problem_rating 
                            FROM problems p 
                            JOIN solved_problems sp ON p.problem_id = sp.problem_id 
                            WHERE sp.user_id = ?''', (user_id,))
            problems = cursor.fetchall()
            
            return [{
                'problem_id': problem[0],
                'contest_id': problem[1],
                'index': problem[2],
                'name': problem[3],
                'rating': problem[4]
            } for problem in problems]
            
    @staticmethod
    def get_total_problems_count() -> int:
        with ConnectionManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM problems')
            return cursor.fetchone()[0]
