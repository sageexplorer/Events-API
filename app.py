from flask import Flask,render_template,redirect,request, url_for, jsonify, make_response, session, abort 
from flask_sqlalchemy import SQLAlchemy 
import json 
from flask_session import Session
from authlib.flask.client import OAuth
from auth import AuthError, requires_auth
from flask_bootstrap import Bootstrap
import http.client

#http://localhost:8100

app = Flask(__name__)
sess = Session()
oauth = OAuth(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qgejdtoiecguax:972ade6d739de4ff4dde8a8ae1555e51764336c0d5630ec37683f48ec05b5d12@ec2-174-129-33-207.compute-1.amazonaws.com:5432/d92hq0j95hh0o6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
audience='event'
client_id='XlgUtmX1H48vmKeyRN7g0SSiin17FQki'

CALLBACK_URL=f'https://https://dev--c9y9ca9.auth0.com/authorize?audience={audience}&response_type=token&client_id={client_id}&redirect_uri=http://localhost:5000/logged'

auth0 = oauth.register(
    'auth0',
    client_id='XlgUtmX1H48vmKeyRN7g0SSiin17FQki',
    client_secret='d6iqtTzn3qDbxPCSYM3DUMn0z7vCNe22-ooFrmOYg7LJ_87tvZ82xjjopx-VWgmK',
    api_base_url='https://dev--c9y9ca9.auth0.com',
    access_token_url='https://dev--c9y9ca9.auth0.com/oauth/token',
    authorize_url='https://dev--c9y9ca9.auth0.com/authorize',
    # callback_url='http://localhost/',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


def get_token():
    conn = http.client.HTTPSConnection("dev--c9y9ca9.auth0.com")
    payload = "{\"client_id\":\"sqgt5Xzn1WX60z069iP7PKk8xkGN9N06\",\"client_secret\":\"70vR1-tWMH_JZxtuHLw4ZIbdLlZd9hZfS_aAAjohqWe6Fr6fb8rf2ritLrAKLHat\",\"audience\":\"event\",\"grant_type\":\"client_credentials\"}"
    headers = { 'content-type': "application/json" }
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print('MYT TOKEN IS',data.decode("utf-8"))
    return data.decode("utf-8")

class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Person(db.Model, JsonModel):
    __tablename__ = 'persons'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(), nullable=False)




    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'



'''create table, and drop table if exists'''
db.create_all()


@app.route('/event/create',methods=['POST'])
def create_events():
    description = request.get_json().get("name")
    todo = Person(name = description)
    db.session.add(todo)
    db.session.commit()
    #return redirect(url_for('index'))
    return jsonify({
        "name": request.get_json().get("name"),
        "status": 200
    })

@app.route('/event/get', methods=['GET'])
def get_events():
    person = Person.query.all()
    return json.dumps([u.as_dict() for u in Person.query.all()])


@app.route('/logout')
def logout():
    return render_template('home.html')


@app.route('/logged', methods=['GET'])

def logged(permission='get:events'):
    try:
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()
        token = get_token()
        # Store the user information in flask session.
        session['jwt_payload'] = userinfo

        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
        return render_template('index.html',userinfo=session['profile'],
                            userinfo_pretty=json.dumps(session['jwt_payload'], indent=4), token=json.dumps(token, indent=4))   
    except:
        abort(404)

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://localhost:5000/logged')

@app.route('/')
def index():
    person = Person.query.all()
    return render_template('home.html')
    # return jsonify({
    #     'name': 'success',
    #     'value':[p for p in person]
    # })

@app.errorhandler(404)
def notfound(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "Not found."
                    }), 404

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)
    app.run()