"""
SubLogger
"""


class SubLogger(object):
  """
  The SubLogger class keeps a record of messages.
  It organizes them hierarchically to preserve
  the notion of sub-problems.

  It is used by the solver to record
  the steps while solving a problem.
  """

  def __init__(self, title="root"):
    self.title = title
    self.entries = []

  def log(self, msg):
    self.entries.append(msg)

  def split(self, *names):
    loggers = [SubLogger(name) for name in names]
    self.entries.append(loggers)
    return loggers
