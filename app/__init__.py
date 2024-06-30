from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = "b'\xcc<\xc5\xfc\n\xbb\x96<R(\rH\xdfv\xcf\xc9A\xc4h\x1d\xf0A\xc3|'"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://skilluser:Fighting.100@localhost/skillbarter'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'signin'

from app import routes, models

# Create database tables before the first request
@app.before_first_request
def create_tables():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))
