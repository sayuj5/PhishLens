import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_FILE = 'users.db'

def setup_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed existing {DB_FILE}")

    # Read usernames
    with open('usernames.txt', 'r') as f:
        usernames = [line.strip() for line in f if line.strip()]
        
    # Read passwords
    with open('passwords.txt', 'r') as f:
        passwords = [line.strip() for line in f if line.strip()]

    if len(usernames) != len(passwords):
        print("Error: The number of usernames and passwords must match.")
        return

    # Connect to SQLite database (this creates it if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Insert seeded users
    for username, password in zip(usernames, passwords):
        password_hash = generate_password_hash(password)
        try:
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        except sqlite3.IntegrityError:
            print(f"User {username} already exists, skipping.")

    conn.commit()
    conn.close()

    print(f"Successfully seeded database with {len(usernames)} users.")

if __name__ == '__main__':
    setup_database()
