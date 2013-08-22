import json

from flask import Flask
from flask import app, make_response, render_template, request
# from flaskext.lesscss import lesscss

from treelogger import TreeLogger
from parseintg import parse
from solver import attempt_integral

app = Flask(__name__)

@app.route("/")
def index():
  # return '<a href"http://localhost:5000/demo">Demo</a>'
  resp = make_response('<a href="/tree">Tree</a>')
  resp.mimetype = 'text/html'
  return resp


@app.route("/API/solve", methods=['GET'])
def api_solve():
  problem_input = request.args.get('problem', u'').encode('ascii', 'ignore')

  log = TreeLogger('root')
  attempt_integral(parse(problem_input), log)

  body = ''
  current_level = -1
  current_logger = 0
  for (level, log, msg) in log.entries:
    if level > current_level:
      body += "<div clas=\"log-level log-level-{}\">".format(level) * (level - current_level)
      current_level = level
    elif level < current_level:
      body += "</div>" * (current_level - level)
      current_level = level

    body += "<span class='{cssclass}'> {msg} </span>".format(cssclass=log.title, msg=msg)
    body += '<br>'

  resp = make_response(body)
  resp.mimetype = 'text/html'
  return resp


@app.route("/tree")
def tree():
  return render_template('tree.html')


if __name__ == "__main__":
  app.run(debug=True)
  # lesscss(app)
