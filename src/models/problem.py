import discord 
from src.models.database.connection import ConnectionManager
from src.data.constants import LITERAL_TAGS, LITERAL_RATING
from typing import Optional
import random

class ProblemManager():

    @staticmethod
    def get_random_problem(tag: Optional[LITERAL_TAGS] = None, rating: Optional[LITERAL_RATING] = None) -> dict:
        with ConnectionManager.get_connection() as conn:
            cursor = conn.cursor()
            if tag:
                if rating:
                    cursor.execute('''
                    SELECT * FROM problems
                    JOIN problem_tags ON problems.problem_id = problem_tags.problem_id
                    JOIN tags ON problem_tags.tag_id = tags.tag_id
                    WHERE tags.tag_name = ?
                    AND problems.problem_rating = ?
                    ORDER BY RANDOM()
                    LIMIT 1
                ''', (tag, rating   ))
                else:
                    cursor.execute('''
                    SELECT * FROM problems
                    JOIN problem_tags ON problems.problem_id = problem_tags.problem_id
                    JOIN tags ON problem_tags.tag_id = tags.tag_id
                    WHERE tags.tag_name = ?
                    ORDER BY RANDOM()
                    LIMIT 1
                ''', (tag,))
                problem = cursor.fetchone()
                print(problem)
                
                problem_tags = cursor.execute('SELECT tag_name FROM problem_tags JOIN tags ON problem_tags.tag_id = tags.tag_id WHERE problem_id = ?', (problem[0],)).fetchall()

                if problem and problem_tags:
                    return {
                        'problem_id': problem[0],
                        'contest_id': problem[1],
                        'index': problem[2],
                        'name': problem[3],
                        'rating': problem[4],
                        'tags': [tag[0] for tag in problem_tags],
                    }
            else:
                
                if rating:
                    problems_count = cursor.execute('SELECT problem_id FROM problems WHERE problem_rating = ?', (rating,)).fetchall()
                else:
                    problems_count = cursor.execute('SELECT problem_id FROM problems').fetchall()
                random_problem_id = random.choice(problems_count)[0]
                print(random_problem_id)

                if rating:
                    problem = cursor.execute('SELECT * FROM problems WHERE problem_rating = ? AND problem_id = ?', (rating, random_problem_id)).fetchone()
                else:
                    problem = cursor.execute('SELECT * FROM problems WHERE problem_id = ?', (random_problem_id,)).fetchone()
                
                print(problem)

                problem_tags = cursor.execute('SELECT tag_name FROM problem_tags JOIN tags ON problem_tags.tag_id = tags.tag_id WHERE problem_id = ?', (problem[0],)).fetchall()

                if problem and problem_tags:
                    return {
                        'problem_id': problem[0],
                        'contest_id': problem[1],
                        'index': problem[2],
                        'name': problem[3],
                        'rating': problem[4],
                        'tags': [tag[0] for tag in problem_tags],
                    }
            return None
