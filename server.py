from functools import wraps
import json
from os import environ as env
from influxdb import InfluxDBClient

from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import request

from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

from strip import turnon, turnoff, state

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'REDACTED'

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='REDACTED',
    client_secret='REDACTED',
    api_base_url='REDACTED',
    access_token_url='REDACTED',
    authorize_url='REDACTED',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

def setupdb():
    client = InfluxDBClient(host='monpi.lan', port=8086)
    client.switch_database('net')

    print(client.get_list_database())

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated

# Controllers API
@app.route('/')
def home():
    if session:
        return render_template('homein.html')
    else:
        return render_template('home.html')
    
# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/smarthome')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback')

@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': 'REDACTED}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@app.route('/smarthome')
@requires_auth
def dashboard():
    if session:
        return render_template('smarthome.html', userinfo=session['profile'],
                            userinfo_pretty=json.dumps(session['jwt_payload'], indent=4), 
                            lstate=state())
        
    else:
        return redirect('/')   

# shelf controls
@app.route('/lightson')
def lightson():
    if session:
        for i in range(0,3):
            turnon(i, "shelfstrip.lan")

        return redirect('/smarthome')

    else:
        return redirect('/')


@app.route('/lightsoff')
def lightsoff():
    if session:
        for i in range(0,3):
            turnoff(i, "shelfstrip.lan")

        return redirect('/smarthome')
        
    else:
        return redirect('/')

#/lighton?num=1&st=strip.lan
@app.route('/lighton')
def lighton():
    if session:
        st = request.args['st']
        num = int(request.args['num'])
        turnon(num, st)
        return redirect('/smarthome')
    else:
        return redirect('/')

#/lightoff?num=1&st=strip.lan
@app.route('/lightoff')
def lightoff():
    if session:
        st = request.args['st']
        num = int(request.args['num'])
        turnoff(num, st)
        return redirect('/smarthome')
    else:
        return redirect('/')

# desk controls

if __name__ == "__main__":
    #setupdb()
    app.run(host='0.0.0.0', port=env.get('PORT', 5000))

#onclick="return confirm('Are you sure?')"