from flask import Flask, request, Response
from functools import wraps
import os
import urllib

app = Flask(__name__)
tenon_api_url = 'http://beta.tenon.io/api/'
key = os.environ.get('TENON_KEY')
username_env = os.environ.get('USERNAME')
password_env = os.environ.get('PASSWORD')

def get_results(url):
  params = urllib.urlencode({'url': url, 'key': key})
  connection = urllib.urlopen(tenon_api_url, params)
  return connection.read()

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

@app.route('/', methods=['GET'])
@requires_auth
def index():
  url = request.args.get('url')
  if keys_set():
    return get_results(url)
  else:
    return 'App working, keys are missing or incorrect'

if __name__ == '__main__':
    app.run()

