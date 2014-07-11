from flask import Flask, request, Response
from functools import wraps
import os

app = Flask(__name__)
key = os.environ.get('TENON_KEY')
username_env = os.environ.get('USERNAME')
password_env = os.environ.get('PASSWORD')

def keys_set():
  return (key != None and username_env != None and password_env != None)

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

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
      return authenticate()
    return f(*args, **kwargs)
  return decorated

@app.route('/')
@requires_auth
def index():
  if keys_set():
    return 'App working, keys are set.'
  else:
    return 'App working, keys are missing or incorrect'

if __name__ == '__main__':
    app.run()

