from flask import Flask, request, Response
from functools import wraps
from tenon import get_results
import os

app = Flask(__name__)
tenon_api_url = 'http://beta.tenon.io/api/'
key = os.environ.get('TENON_KEY')
username_env = os.environ.get('USERNAME')
password_env = os.environ.get('PASSWORD')
origins_env = os.environ.get('ORIGINS')
origins = origins_env.split(' ') if origins_env != None else None

def check_origin(origin):
  try:
    idx = origins.index(origin)
    return origins[idx]
  except ValueError:
    return false

def keys_set():
  return (key != None and username_env != None and password_env != None and origins != None)

def app_setup_fail():
  """Responds to environment variables being set up incorrectly"""
  return Response(
      'Sorry, we are having technical difficulties\n'
      'Please try again in a few minutes', 500)

def check_auth(username, password):
  """This function is called to check if a username /
  password combination is valid.
  """
  return username == username_env and password == password_env

def authenticate():
  """Sends a 401 response that enables basic auth"""
  return Response(
  'Could not verify your access level for that URL.\n'
  'You have to login with proper credentials', 401,
  {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_setup(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if not keys_set():
      return app_setup_fail()
    return f(*args, **kwargs)
  return decorated

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
      return authenticate()
    return f(*args, **kwargs)
  return decorated

@app.route('/', methods=['GET'])
@requires_setup
@requires_auth
def index():
  origin = check_origin(request.headers['Origin'])
  params = request.args.items()
  params.append(( 'key', key ))
  results = get_results(tenon_api_url, params)
  response = Response(results, 200,
  {'Content-Type': 'application/json; charset=utf-8'})
  if origin:
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Origin', origin)
  return response

if __name__ == '__main__':
    app.run()

