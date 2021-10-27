from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sergazin@localhost:5432/JWT'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    token = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return '<Users %r>' % self.username

db.create_all()
