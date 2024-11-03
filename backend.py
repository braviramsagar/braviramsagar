from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traceability.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)  # 'Farmer' or 'Customer'

# Initialize the database
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['POST'])
def register():
    full_name = request.form.get('fullName')
    email = request.form.get('email')
    password = request.form.get('password')
    user_type = request.form.get('userType')

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        flash('Email address already registered.')
        return redirect(url_for('home'))

    # Create a new user
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(full_name=full_name, email=email, password=hashed_password, user_type=user_type)
    db.session.add(new_user)
    db.session.commit()

    flash('Registration successful! Please log in.')
    return redirect(url_for('home'))

# Login route
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    # Check if user exists and password matches
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['user_type'] = user.user_type
        flash('Login successful!')
        return redirect(url_for('dashboard'))

    flash('Invalid credentials. Please try again.')
    return redirect(url_for('home'))

# Dashboard route (after login)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('home'))

    user_type = session.get('user_type')
    return render_template('dashboard.html', user_type=user_type)

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
