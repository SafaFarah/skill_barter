from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255), default='default_profile.jpg')
    bio = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    skills_i_have = db.Column(db.String(255))
    skills_i_want = db.Column(db.String(255))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
