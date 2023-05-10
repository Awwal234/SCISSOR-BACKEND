from ..utils import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(6), nullable=False, unique=True)
    link = db.relationship('LinkModel', backref='links', lazy=True)
    
    def __repr__(self):
        return f"SignUp('{self.name}')"
        
    def save(self):
        db.session.add(self)
        db.session.commit()