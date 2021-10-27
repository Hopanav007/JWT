from flask import Flask
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
import jwt
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import time
import datetime
from datetime import date,timedelta


app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sergazin@localhost:5432/JWT'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    token = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return '<Users %r>' % self.login

# db.create_all()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'This is only available for people with valid tokens.'})

@app.route('/login')
def login():
    auth = request.authorization

    if auth and (Users.query.filter_by(login=auth.username).first()!=None):
        if (Users.query.filter_by(login=auth.username).first().password == auth.password):
            token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=60)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run(debug=True)