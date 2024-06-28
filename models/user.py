# models/user.py
import uuid
from . import db
from .skill import Skill  # Assuming Skill model is defined in skill.py

class User(db.Model):
    __tablename__ = 'users'

    ID = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # Define relationships after both classes have been defined
    skills = db.relationship('Skill', backref='user', lazy=True)
    barters = db.relationship('Barter', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.ID = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        return f"[User] ({self.id}) {self.username}"

