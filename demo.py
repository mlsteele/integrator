from elements import *
from strategies import *
from parser import parse

class Logger(object):
  def __init__(self):
    self.buffer = ''

  def log(self, string):
    self.buffer += str(string) + '\n'

  def dump(self):
    return self.buffer

logger = Logger()

def attempt_intgral(expr):
  logger.log("I will attempt to solve %s." % expr)
  expr = expr.simplified()
  logger.log("I can simplify it to %s." % expr)

  if isinstance(expr, Integral):
    logger.log("%s is an integral" % expr)

    for strategy in STRATEGIES:
      if strategy.applicable(expr):
        logger.log("I will use the %s rule" % strategy.description)
        return attempt_intgral(strategy.apply(expr))

    logger.log("I think I'm stuck.")
    return expr
  elif isinstance(expr, Sum):
    logger.log("%s is a sum" % expr)
    logger.log("I will solve the two sub-problems of %s and %s" %(expr.a, expr.b))
    logger.log("")
    logger.log("subproblem:")
    sub_a = attempt_intgral(expr.a)
    logger.log("subproblem:")
    sub_b = attempt_intgral(expr.b)
    return Sum(sub_a, sub_b)
  else:
    logger.log("%s is not an integral, I think I'm stuck." % expr)
    return expr

def run():
  ss = ["intxdx", "intx^2dx", "int 3 x^(2 * 3) dx", "int x + 3 dx"]
  for s in ss:
    expr = parse(s)
    logger.log(expr)
    logger.log("\n end result: %s" % attempt_intgral(expr))
    logger.log(2 * "\n")
    logger.log("-----")
    logger.log(2 * "\n")

if __name__ == "__main__":
  run()
  print logger.dump()
