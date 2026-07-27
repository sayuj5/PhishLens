from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import logging
import time

app = Flask(__name__)
app.secret_key = 'super_secret_cyber_key'

# Configure logging to a file
logging.basicConfig(
    filename='login_attempts.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Flask-Limiter for rate limiting
# This limits each IP to 50 requests per minute overall, and 10 per minute on the login route
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["50 per minute"],
    storage_uri="memory://"
)

DB_FILE = 'users.db'

# In-memory store for account lockouts (Username -> (Failed Count, Lockout Expiry Timestamp))
# For a real application, this should be stored in the database!
account_lockouts = {}
LOCKOUT_DURATION = 60 # Lockout for 60 seconds after 5 failed attempts
MAX_FAILED_ATTEMPTS = 5

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute") # Rate limiting: Slows down brute force
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if account is locked out
        if username in account_lockouts:
            attempts, lockout_expiry = account_lockouts[username]
            if time.time() < lockout_expiry:
                logging.warning(f"BLOCKED LOGIN: Account {username} is currently locked out.")
                flash('Account locked due to too many failed attempts. Try again later.')
                return render_template('login.html')
            else:
                # Lockout period expired, reset attempts
                del account_lockouts[username]

        # Database lookup
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        # Verify password
        if user and check_password_hash(user['password_hash'], password):
            logging.info(f"SUCCESSFUL LOGIN: {username}")
            # Reset failed attempts on success
            if username in account_lockouts:
                del account_lockouts[username]
                
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            logging.warning(f"FAILED LOGIN: Invalid credentials for {username}")
            
            # Increment failed attempts
            if username not in account_lockouts:
                account_lockouts[username] = [1, 0]
            else:
                account_lockouts[username][0] += 1
                
            # Trigger lockout if max attempts reached
            if account_lockouts[username][0] >= MAX_FAILED_ATTEMPTS:
                account_lockouts[username][1] = time.time() + LOCKOUT_DURATION
                logging.warning(f"ACCOUNT LOCKED: {username} locked for {LOCKOUT_DURATION} seconds.")
                flash('Account locked due to too many failed attempts. Try again later.')
            else:
                flash('Invalid username or password')
                
            return render_template('login.html')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
