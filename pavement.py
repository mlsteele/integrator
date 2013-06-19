from paver.easy import *
import os
import subprocess

TASK_ROOT = os.path.dirname(os.path.realpath(__file__))

@task
def tests():
  """ Run the unit tests and generate coverage report. """
  subprocess.call("nosetests --with-coverage --cover-erase --cover-tests --cover-html".split(' '))


@task
@needs(['tests'])
def testsopen():
  """ Run tests and open html report (only osx?) """
  import webbrowser
  webbrowser.open("file://{}/cover/index.html".format(TASK_ROOT))


@task
def server():
  # import webbrowser
  # webbrowser.open("http://localhost:5000")
  subprocess.call("python web.py".split(' '))


@task
def taskdebug():
  """ Stuff for debugging paver tasks. """
  print "__name__: {}".format(__name__)
  print "__file__: {}".format(__file__)
  print "os.path.abspath(__file__): {}".format(os.path.abspath(__file__))
  print "os.path.realpath(__file__): {}".format(os.path.realpath(__file__))
  print "os.path.dirname(os.path.realpath(__file__)): {}".format(os.path.dirname(os.path.realpath(__file__)))
