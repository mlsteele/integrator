from flask import Flask
from flask import app, make_response, render_template
# from flaskext.lesscss import lesscss

from treelogger import TreeLogger
from parseintg import parse
from doodle import attempt_integral

app = Flask(__name__)

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

  body = ''
  for (level, log, msg) in log.entries:
    body += "<span class='{cssclass}'> {msg} </span>".format(cssclass=log.title, msg=msg)
    body += '<br>'

  return render_template('tree.html', raw_content=body)


if __name__ == "__main__":
  app.run(debug=True)
  # lesscss(app)
