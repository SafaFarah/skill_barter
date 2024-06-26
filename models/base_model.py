#!/usr/bin/python3
import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel:
    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        """
        Initialize a new instance of BaseModel.
        Args:
            **kwargs: dictionary of arguments.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        """
        Update the updated_at attribute and save the instance to the database.
        """
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        """
        Convert instance attributes to a dictionary for serialization.
        Returns:
            dict: A dictionary containing all instance attributes.
        """
        instance_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        instance_dict["created_at"] = self.created_at.isoformat()
        instance_dict["updated_at"] = self.updated_at.isoformat()
        return instance_dict

    @classmethod
    def load_all(cls):
        """
        Load all instances of the class from the database.
        Returns:
            list: A list of instances of the class.
        """
        return cls.query.all()

    def __str__(self):
        """
        Return a string representation of the instance.
        Returns:
            str: A string representation of the instance.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

