from ..utils import db
from datetime import datetime

class LinkModel(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    link = db.Column(db.String(200), nullable=False)
    short_link = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"link('{self.link}')"
        
    def save(self):
        db.session.add(self)
        db.session.commit()