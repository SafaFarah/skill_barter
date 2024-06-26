#!/usr/bin/python3

from app import db
from models.base_model import BaseModel

class User(BaseModel, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)

    skills = db.relationship('Skill', backref='user', lazy=True)
    barters = db.relationship('Barter', backref='user', lazy=True)

    def __init__(self, username, email, password, profile_picture=None, **kwargs):
        """
        Initialize a new instance of User.
        
        Args:
            username (str): The username of the user.
            email (str): The email of the user.
            password (str): The password of the user.
            profile_picture (str, optional): The profile picture of the user. Defaults to None.
            **kwargs: Additional keyword arguments for initializing the BaseModel.
        """
        super().__init__(**kwargs)
        self.username = username
        self.email = email
        self.password = password
        self.profile_picture = profile_picture

    def __str__(self):
        """
        Return a string representation of the instance.

        Returns:
            str: A string representation of the instance.
        """
        return f"[User] ({self.id}) {self.__dict__}"

