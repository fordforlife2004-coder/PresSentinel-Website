import datetime
import hashlib
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tip(db.Model):
    __tablename__ = 'tips'
    
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), unique=True, nullable=False, index=True)
    jurisdiction = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text, nullable=False)
    callback_alias = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    verification_hash = db.Column(db.String(64), nullable=False)

    @staticmethod
    def generate_hash(token: str, details: str) -> str:
        payload = f"{token}:{details}".encode('utf-8')
        return hashlib.sha256(payload).hexdigest()
