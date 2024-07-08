from . import db

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # String representation of the Skill instanc
    def __repr__(self):
        return f'<Skill {self.name}>'

