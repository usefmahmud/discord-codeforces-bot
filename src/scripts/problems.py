'''
This script is used to add the problems and tags in the database.
'''
import sqlite3
from src.api.codeforces import cf_client

tags = [
  "2-sat",
  "binary search",
  "bitmasks",
  "brute force",
  "chinese remainder theorem",
  "combinatorics",
  "constructive algorithms",
  "data structures",
  "dfs and similar",
  "divide and conquer",
  "dp",
  "dsu",
  "expression parsing",
  "fft",
  "flows",
  "games",
  "geometry",
  "graph matchings",
  "graphs",
  "greedy",
  "hashing",
  "implementation",
  "interactive",
  "math",
  "matrices",
  "meet-in-the-middle",
  "number theory",
  "probabilities",
  "schedules",
  "shortest paths",
  "sortings",
  "string suffix structures",
  "strings",
  "ternary search",
  "trees",
  "two pointers",
  "*special"
]

conn = sqlite3.connect('src/data/bot.db')
cursor = conn.cursor()

problems = cf_client.get_problems()
i = 1
for problem in problems:
    rating = problem['rating'] if 'rating' in problem else 0

    cursor.execute('''
          INSERT INTO problems (contest_id, problem_name, problem_index, problem_rating) 
          VALUES (?, ?, ?, ?)''', (problem['contestId'], problem['name'], problem['index'], rating))


    for tag in problem['tags']:
        tags.index(tag)
        cursor.execute('''
          INSERT INTO problem_tags (problem_id, tag_id) 
          VALUES (?, ?)''', (i, tags.index(tag) + 1))
        
    i += 1

conn.commit()

conn.close()
