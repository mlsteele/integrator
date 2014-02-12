import json

from flask import Flask
from flask import app, make_response, render_template, request
# from flaskext.lesscss import lesscss

from sublogger import SubLogger
from parseintg import parse
from solver import attempt_integral

app = Flask(__name__)

def sublog_to_html(logger):
  html = ""
  html += "<div class=\"subproblem\">"
  for entry in logger.entries:
    if isinstance(entry, list):
      for sublogger in entry:
        html += sublog_to_html(sublogger)
      html += "<div class=\"clearbar\"></div>"
    else:
      html += "<span>{msg}</span><br>".format(msg=entry)

  html += "</div>"
  return html

@app.route("/API/solve", methods=['GET'])
def api_solve():
  problem_input = request.args.get('problem', u'').encode('ascii', 'ignore')

  log = SubLogger('root')
  attempt_integral(parse(problem_input), log)
  body = sublog_to_html(log)

  resp = make_response(body)
  resp.mimetype = 'text/html'
  return resp


@app.route("/")
def solver():
  return render_template('solver.html')


if __name__ == "__main__":
  app.run(debug=True)
  # lesscss(app)
