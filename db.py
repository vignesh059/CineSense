import sqlite3
import os

DATABASE = 'reviews.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Using IF NOT EXISTS. If you want to force recreate, you'd need to drop it,
    # but let's just make sure the table has the right columns or is recreated.
    # We can check if 'rnn_sentiment' exists, if not, drop the table and recreate.
    
    cursor.execute("PRAGMA table_info(reviews)")
    columns = [col['name'] for col in cursor.fetchall()]
    if columns and 'rnn_sentiment' not in columns:
        print("Schema changed. Dropping old reviews table...")
        cursor.execute("DROP TABLE reviews")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            movie_id TEXT NOT NULL,
            review_text TEXT NOT NULL,
            rnn_sentiment TEXT NOT NULL,
            lstm_sentiment TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
