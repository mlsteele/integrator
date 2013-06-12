from flask import Flask
from flask import app, make_response, render_template
app = Flask(__name__)

import demo

@app.route("/")
def index():
  # return '<a href"http://localhost:5000/demo">Demo</a>'
  resp = make_response('<a href="/demo">Demo</a>')
  resp.mimetype = 'text/html'
  return resp

@app.route("/demo")
def hello():
  demo.run()
  return demo.logger.dump().replace('\n', '<br>')

if __name__ == "__main__":
  app.run()
