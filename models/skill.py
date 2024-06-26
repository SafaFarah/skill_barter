#!/usr/bin/python3

from app import db
from models.base_model import BaseModel

class Skill(BaseModel, db.Model):
    __tablename__ = 'skills'

    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name, description, user_id, **kwargs):
        """
        Initialize a new instance of Skill.
        
        Args:
            name (str): The name of the skill.
            description (str): The description of the skill.
            user_id (str): The ID of the user who has this skill.
            **kwargs: Additional keyword arguments for initializing the BaseModel.
        """
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.user_id = user_id

    def __str__(self):
        """
        Return a string representation of the instance.

        Returns:
            str: A string representation of the instance.
        """
        return f"[Skill] ({self.id}) {self.__dict__}"

