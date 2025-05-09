import sqlite3

conn = sqlite3.connect('src/data/bot.db')
cursor = conn.cursor()

# 1. Create a new table with the correct schema
cursor.execute('''
CREATE TABLE users_new (
    user_id INTEGER PRIMARY KEY,
    name TEXT,           -- now allows NULL
    handle TEXT,         -- now allows NULL
    verified INTEGER DEFAULT 0,
    verification_code TEXT,
    rank TEXT DEFAULT 'unrated',
    rating INTEGER DEFAULT 0,
    points INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# 2. Copy data from the old table to the new table
cursor.execute('''
INSERT INTO users_new (user_id, name, handle, verified, verification_code, rank, rating, points, created_at, updated_at)
SELECT user_id, name, handle, verified, verification_code, rank, rating, 0, created_at, updated_at FROM users
''')

# 3. Drop the old table
cursor.execute('DROP TABLE users')

# 4. Rename the new table to the original name
cursor.execute('ALTER TABLE users_new RENAME TO users')

conn.commit()

conn.close()