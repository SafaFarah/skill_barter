from app import db

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    barter_id = db.Column(db.Integer, db.ForeignKey('barter.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    
    user = db.relationship('User', backref='requests')
    barter = db.relationship('Barter', backref='requests')

    def __init__(self, user_id, barter_id, status='pending'):
        self.user_id = user_id
        self.barter_id = barter_id
        self.status = status

