class SubLogger(object):
  def __init__(self, title="root"):
    self.title = title
    self.entries = []

  def log(self, msg):
    self.entries.append(msg)

  def split(self, *names):
    loggers = [SubLogger(name) for name in names]
    self.entries.append(loggers)
    return loggers


if __name__ == "__main__":
  pass
  # logger = SubLogger()
  # logger.log("Hello")
  # logger.log("I'm going to solve a problem.")
  # logger.log("It has two parts.")
  # part1, part2 = logger.split("Part 1", "Part 2")
  # logger.log("Now that those are done, let's use their results.")
