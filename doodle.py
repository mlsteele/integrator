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
    return expr
  elif isinstance(expr, Sum):
    print "%s is a sum" % expr
    print "I will solve the two sub-problems of %s and %s" %(expr.a, expr.b)
    print ""
    print "subproblem:"
    sub_a = attempt_intgral(expr.a)
    print "subproblem:"
    sub_b = attempt_intgral(expr.b)
    return Sum(sub_a, sub_b)
  else:
    print "%s is not an integral, I think I'm stuck." % expr
    return expr

if __name__ == "__main__":
  # attempt_intgral(parse("intx^2dx"))
  # attempt_intgral(parse("(1.0 / 3.0) * (x ^ 3.0)"))
  # print Fraction(Number(4), Number(2)).simplified()
  # print attempt_intgral(parse("intxdx"))
  # print attempt_intgral(parse("((1 / 2) * (x ^ 2))"))
  print Product(Number(2), Number('1'))
