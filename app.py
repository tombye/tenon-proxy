from flask import Flask, request
import os

app = Flask(__name__)
key = os.environ.get('TENON_KEY')

@app.route('/')
def index():
    return 'App working'

@app.route('/')
def index():
  if key != None:
    return 'App working, key is set.'
  else:
    return 'App working, no key set.'

if __name__ == '__main__':
    app.run()


