from . import db
from .base_model import BaseModel

class Barter(BaseModel, db.Model):
    __tablename__ = 'barters'

    id = db.Column(db.Integer, primary_key=True)
    skill_offered = db.Column(db.String(80), nullable=False)
    skill_requested = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, skill_offered, skill_requested, user_id, **kwargs):
        super().__init__(**kwargs)
        self.skill_offered = skill_offered
        self.skill_requested = skill_requested
        self.user_id = user_id

    def __str__(self):
        return f"[Barter] ({self.id}) Offered: {self.skill_offered}, Requested: {self.skill_requested}, User: {self.user_id}"

