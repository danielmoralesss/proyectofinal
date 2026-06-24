from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(300))
    scraped = db.Column(db.Boolean, default=False)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300))
    content = db.Column(db.Text)
    year = db.Column(db.Integer)