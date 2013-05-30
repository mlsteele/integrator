from elements import *
from strategies import *
from parser import parse

def attempt_intgral(expr):
  print "I will attempt to solve %s." % expr
  expr = expr.simplified()
  print "I can simplify it to %s." % expr

  if isinstance(expr, Integral):
    print "%s is an integral" % expr

    for strategy in STRATEGIES:
      if strategy.applicable(expr):
        print "I will use the %s rule" % strategy.description
        return attempt_intgral(strategy.apply(expr))

    print "I think I'm stuck."
  else:
    print "%s is not an integral, I think I'm stuck." % expr

if __name__ == "__main__":
  s = "intx^2dx"
  expr = parse(s)
  attempt_intgral(expr)
