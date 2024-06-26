from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://skilluser:Fighting.100@localhost/skillbarter'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes 

# Create database tables before the first request
@app.before_first_request
def create_tables():
    db.create_all()

from models.user import User
from models.barter import Barter
from models.skill import Skill
from models.barter import Barter
from models.base_model import BaseModel

