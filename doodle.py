from elements import *
from strategies import *
from parseintg import parse
from treelogger import TreeLogger

def attempt_integral(expr_raw, log):
  log.push("I will attempt to solve %s." % expr_raw.latex())
  expr = expr_raw.simplified()
  if expr != expr_raw:
    log.push("I can simplify it to %s." % expr.latex())

  if isinstance(expr, Integral):
    log.push("%s is an integral" % expr.latex())

    log.push("Which of my strategies are applicable to this integral?")
    for strategy in STRATEGIES:
      if strategy.applicable(expr):
        log.push("The {} rule is applicable, I will try it".format(strategy.description))
        applied = strategy.apply(expr)
        return attempt_integral(applied, log)
      else:
        log.push("The {} rule is not applicable".format(strategy.description))

    log.push("None of my integration strategies will work. I think I'm stuck.")
    return expr
  elif isinstance(expr, Sum):
    log.push("{} is a sum. I will solve the two sub-problems and then add the results.".format(expr.latex()))
    sub_a = attempt_integral(expr.a, log.split('subproblem-a'))
    sub_b = attempt_integral(expr.b, log.split('subproblem-b'))
    combined = Sum(sub_a, sub_b)
    log.push("I will add the results of the sub-problems back together to get {}.".format(combined.latex()))
    return combined
  else:
    log.push("{} is not an integral, good enough.".format(expr))
    return expr

if __name__ == "__main__":
  log = TreeLogger('root')
  attempt_integral(parse("intxdx"), log)
  print log.dump()
