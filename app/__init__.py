from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://skilluser:Fighting.100@localhost/skillbarter'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
UPLOAD_FOLDER = 'app/static/profile_pics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'signin'  # Specify the login view

# Import routes at the end to avoid circular imports
from app import routes

# Create database tables before the first request
@app.before_first_request
def create_tables():
    db.create_all()

# Import models to ensure they are registered with SQLAlchemy
from models.user import User
from models.barter import Barter
from models.skill import Skill
from models.barter_response import BarterResponse
from models.request import Request 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

