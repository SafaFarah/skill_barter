from app import db

class Barter(db.Model):
    __tablename__ = 'barter'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    skill_offered = db.Column(db.String(100))
    skill_requested = db.Column(db.String(100))
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    status = db.Column(db.String(50), default='available')  # 'available', 'requested', 'accepted'

    user = db.relationship('User', foreign_keys=[user_id], back_populates='barters_created')
    requester = db.relationship('User', foreign_keys=[requester_id], back_populates='barters_requested')

    def __repr__(self):
        return f'<Barter {self.title}>'

