from app import db
from datetime import datetime

class BarterResponse(db.Model):
    __tablename__ = 'barter_response'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=True)
    offered_skill = db.Column(db.String(100), nullable=False)
    requested_skill = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to reference the barter
    barter_id = db.Column(db.Integer, db.ForeignKey('barter.id'), nullable=False)
    
    # Foreign key to reference the user who responded to the barter
    responder_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"BarterResponse('{self.offered_skill}', '{self.requested_skill}')"

