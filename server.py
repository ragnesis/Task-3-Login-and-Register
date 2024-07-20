from flask import Flask, request, redirect, url_for, send_from_directory
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mayank0510//",
    database="Register"
)

cursor = db.cursor()

# Create users table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
)
""")

@app.route('/')
def index():
    return send_from_directory('.', 'auth.html')

@app.route('/portfolio')
def portfolio_page():
    return send_from_directory('.', 'portfolio_index.html')

@app.route('/<path:filename>')
def serve_files(filename):
    return send_from_directory('.', filename)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    # Debug: Print received email and password (omit in production)
    print(f"Attempting login with email: {email}")

    # Fetch user from database
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    
    # Debug: Print fetched user
    print(f"Fetched user: {user}")

    if user:
        # Check if password matches the hashed password
        if check_password_hash(user[2], password):
            return redirect(url_for('portfolio_page'))  # Redirect on successful login
        else:
            print("Password does not match.")
    else:
        print("No user found with that email.")

    return redirect(url_for('index'))  # Redirect back to login page on failure

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        return "Passwords do not match!"
    
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    try:
        cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, hashed_password))
        db.commit()
        return redirect(url_for('index'))  # Redirect to auth.html on successful registration
    except mysql.connector.IntegrityError:
        return "Email already registered!"

if __name__ == '__main__':
    app.run(debug=True)
