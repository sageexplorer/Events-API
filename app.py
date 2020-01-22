from flask import Flask,render_template,redirect,request, url_for, jsonify, make_response, session, abort 
from flask_sqlalchemy import SQLAlchemy 
import json 
from flask_session import Session
from authlib.flask.client import OAuth
from auth import AuthError, requires_auth
from flask_bootstrap import Bootstrap
import os 
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path  
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


app = Flask(__name__)
sess = Session()
oauth = OAuth(app)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

audience='event'
CLIENT_ID= os.environ.get('CLIENT_ID', None)
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', None)
CALLBACK_URL = 'http://localhost:5000/logged'
AUTH_URL = os.environ.get('AUTH_URL', None)

auth0 = oauth.register(
    'auth0',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    api_base_url=AUTH_URL,
    access_token_url=f'{AUTH_URL}/oauth/token',
    authorize_url=f'{AUTH_URL}/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def serialize(self):
            return {
                'name': self.name,
                'user_id':self.id
            }    

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    website = db.Column(db.String(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Person.id), foreign_key=True)

    def serialize(self):
            return {
                'event_id': self.id,
                'user_id': self.user_id,
                'event': self.event,
                'data': self.date,
                'location': self.location,
                'website': self.website
            }    


'''create table, and drop table if exists'''
db.create_all()


@app.route('/create/events', methods=['POST'])
@requires_auth('post:events')
def new_event(permission=''):
    try:
        id = request.get_json().get("user_id")
        event = request.get_json().get("event")
        date = request.get_json().get("date")
        location = request.get_json().get("location")
        website = request.get_json().get("website")
        data = Event(event=event, date=date,location=location, website=website, user_id=id)
        db.session.add(data)
        db.session.commit()
        return jsonify({
            "events": "event created",
            "status": 200
        })
    except Exception as e:
        print("MY ERROR IS",e)
        abort(403)


@app.route('/create/user',methods=['POST'])
def create_user():
    user_id = request.get_json().get("id")
    name  = request.get_json().get("name")
    data = Person(id=user_id, name=name)
    db.session.add(data)
    db.session.commit()
    return jsonify({
        "name": request.get_json().get("name"),
        "status": 200
    })
   

@app.route('/get/users')
def get_user():
    users = Person.query.all()
    return jsonify({
        "user": [u.serialize() for u in users],
        "status": 200
    })   


    
''' Managers can get all events, users(public) can only get their own events'''
@app.route('/get/events', methods=['GET'])
@requires_auth('get:events')
def get_events(permission=''):
    id = request.get_json().get("id")
    events =  db.session.query(Event).filter(Event.user_id == id).all()
    print(events)
    return jsonify({
       "events": [event.serialize() for event in events],
       "success": True
    })

@app.route('/get/all/events')
@requires_auth('get:allevents')
def get_all_events(permission):
    try:
        events =  Event.query.all()
        print(events)
        return jsonify({
        "events": [event.serialize() for event in events],
        "success": True
        })
    except Error:
        abort(401)


@app.route('/patch/events', methods=['PATCH'])
@requires_auth('patch:events')
def patch_events(permission):
    event_id = request.get_json().get("id")
    my_event = db.session.query(Event).filter(Event.id == event_id).first()
    user_id = request.get_json().get("user_id")
    try:
        event = request.get_json().get("event")
        my_event.event = event
        date = request.get_json().get("date")
        my_event.date = date
        location = request.get_json().get("location")
        my_event.location = location
        website = request.get_json().get("website")
        my_event.website = website
        
        db.session.commit()
        return jsonify ({
            "success": True
        })
    except Exception as e:
        print("MY ERROR IS", e )
        abort(401)    

@app.route('/delete/events', methods=['DELETE'])
@requires_auth('delete:events')
def delete_events(permission):
    event_id = request.get_json().get("id")
    my_event = db.session.query(Event).filter(Event.id == event_id).first()
    try:
        db.session.delete(my_event)
        db.session.commit()
        return jsonify ({
            "success": True
        })
    except Exception as e:
        print("MY ERROR IS", e )
        abort(401)


@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')


@app.route('/logged', methods=['GET'])
def logged():
    try:
        res = auth0.authorize_access_token()
        token = res.get('access_token')
        session['jwt_token'] = token
        print('MY TOKEN IS***', token) 
        return render_template('index.html', token=session['jwt_token'])                          
    except Exception as e:
        print('MY ERORR IS',e)
        abort(404)

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=CALLBACK_URL, audience='event')

@app.route('/')
def index():
    return render_template('home.html')

@app.errorhandler(404)
def notfound(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found."
        }), 404

@app.errorhandler(403)
def notauthorized(error):
    return jsonify({
        "success": False, 
        "error": 403,
        "message": "Not Authorized."
        }), 403

if __name__ == '__main__':
    app.secret_key = 'sdlkjweioewlknwlkejlwkejlk'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
