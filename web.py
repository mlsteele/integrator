from flask import Flask
from flask import app, make_response, render_template
app = Flask(__name__)

from treelogger import TreeLogger
from parseintg import parse
from doodle import attempt_integral


@app.route("/")
def index():
  # return '<a href"http://localhost:5000/demo">Demo</a>'
  resp = make_response('<a href="/tree">Tree</a>')
  resp.mimetype = 'text/html'
  return resp


@app.route("/tree")
def tree():
  log = TreeLogger('root')
  attempt_integral(parse("intxdx"), log)
  body = '<br>'.join([msg for (level, log, msg) in log.entries])

  resp = make_response(body)
  resp.mimetype = 'text/html'
  return resp


if __name__ == "__main__":
  app.run(debug=True)
