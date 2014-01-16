from elements import *
from strategies import *
from parseintg import parse
from sublogger import SubLogger

def latex_wrap(s):
  return "\( {} \)".format(s)

def attempt_integral(expr_raw, logger):
  logger.log("I will attempt to solve %s." % latex_wrap(expr_raw.latex()))
  expr = expr_raw.simplified()
  if expr != expr_raw:
    logger.log("I can simplify it to %s." % latex_wrap(expr.latex()))

  if isinstance(expr, Integral):
    logger.log("%s is an integral" % latex_wrap(expr.latex()))

    logger.log("Which of my strategies are applicable to this integral?")
    for strategy in STRATEGIES:
      if strategy.applicable(expr):
        logger.log("The \"{}\" rule is applicable, I will try it".format(strategy.description))
        applied = strategy.apply(expr)
        return attempt_integral(applied, logger)
      else:
        logger.log("The \"{}\" rule is not applicable".format(strategy.description))

    logger.log("None of my integration strategies will work. I think I'm stuck.")
    return expr
  elif isinstance(expr, Sum):
    logger.log("{} is a sum. I will solve the two sub-problems and then add the results.".format(latex_wrap(expr.latex())))
    subproblem_a, subproblem_b = logger.split('subproblem-a', 'subproblem-b')
    sub_a = attempt_integral(expr.a, subproblem_a)
    sub_b = attempt_integral(expr.b, subproblem_b)
    combined = Sum(sub_a, sub_b)
    logger.log("I will add the results of the sub-problems back together to get {}.".format(latex_wrap(combined.latex())))
    return combined
  else:
    logger.log("{} is not an integral, good enough.".format(latex_wrap(expr.latex())))
    return expr

if __name__ == "__main__":
  # log = SubLogger('root')
  # attempt_integral(parse("intxdx"), log)
  # print logger.dump()

  log = SubLogger('root')
  attempt_integral(parse("3 / 4"), log)
  print logger.dump()




def dxh_test():
  vset = VariableSet()
  x = vset.variable("x")
  q = Fraction(Number(1), x)
  attempt_integral(Integral(q,x),SubLogger())
