from elements import *
from strategies import *
from parseintg import parse
from treelogger import TreeLogger

def attempt_integral(expr, log):
  log.push("I will attempt to solve %s." % expr)
  expr = expr.simplified()
  log.push("I can simplify it to %s." % expr)

  if isinstance(expr, Integral):
    log.push("%s is an integral" % expr)

    for strategy in STRATEGIES:
      if strategy.applicable(expr):
        log.push("I will use the %s rule" % strategy.description)
        return attempt_integral(strategy.apply(expr), log)

    log.push("I think I'm stuck.")
    return expr
  elif isinstance(expr, Sum):
    log.push("%s is a sum" % expr)
    log.push("I will solve the two sub-problems of %s and %s" %(expr.a, expr.b))
    sub_a = attempt_integral(expr.a, log.split('subproblem-a'))
    sub_b = attempt_integral(expr.b, log.split('subproblem-b'))
    return Sum(sub_a, sub_b)
  else:
    log.push("%s is not an integral, I think I'm stuck." % expr)
    return expr


if __name__ == "__main__":
  ss = ["intxdx", "intx^2dx", "int 3 x^(2 * 3) dx", "int x + 3 dx"]
  for s in ss:
    expr = parse(s)
    log = TreeLogger('root')
    result = attempt_integral(parse(s), log)
    print log.dump()
    print result

    print 2 * "\n"
    print '-' * 5
    print 2 * "\n"

