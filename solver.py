"""
Integration Solver

attempt_integral is the main method of this module.
It will attempt to solve an expression which could
contain an integral.
"""

import inspect

from elements import *
from strategies import *
from parseintg import parse
from sublogger import SubLogger

def latex_wrap(s):
  """
  Wrap a string in delimeters to mark it for LaTeX rendering.
  """
  return "\( {} \)".format(s)

def newlines_to_breaks(s):
  """
  Convert newlines in a string into html break elements.
  """
  return s.replace("\n", "<br>")

def attempt_integral(expr_raw, logger):
  """
  attempt_integral is a recursive function which takes
  an expressions and attempts to simplify it.

  attempt_integral will break the problem down
  into sub-problems to try to solve the simplest
  problems first and then compound the results.

  If there are integrals in the expression, then
  attempt_integral will go through its booklet
  of strategies (from the strategies module)
  and find one to apply to attempt to solve
  or simplify the integral.
  """
  logger.log("I will attempt to solve %s." % latex_wrap(expr_raw.latex()))
  expr = expr_raw.simplified()
  if expr != expr_raw:
    logger.log("I can simplify it to %s." % latex_wrap(expr.latex()))

  # if the expression is an integral then try the integration strategies
  if expr.is_a(Integral):
    logger.log("%s is an integral." % latex_wrap(expr.latex()))

    logger.log("Which of my strategies are applicable to this integral?")
    for strategy in STRATEGIES:
      if strategy.applicable(expr):
        strategy_source = newlines_to_breaks(inspect.getsource(strategy))
        strategy_info = '<div class="strategy-icon"><div class="strategy-code"><pre>{}</pre></div></div>'.format(
          strategy_source
        )

        logger.log("The \"{}\" rule {} is applicable, I will try it.".format(
          strategy.description,
          strategy_info))

        applied = strategy.apply(expr)
        return attempt_integral(applied, logger)
      else:
        # logger.log("The \"{}\" rule is not applicable.".format(strategy.description))
        pass

    logger.log("None of my integration strategies will work. I think I'm stuck.")
    return expr

  # if the expression is a sum or product then break it into to sub-problems.
  elif expr.is_a(Sum):
    logger.log("{} is a sum. I will solve the two sub-problems and then add the results.".format(latex_wrap(expr.latex())))
    subproblem_a, subproblem_b = logger.split('subproblem-a', 'subproblem-b')
    sub_a = attempt_integral(expr.a, subproblem_a)
    sub_b = attempt_integral(expr.b, subproblem_b)
    combined = Sum(sub_a, sub_b)
    logger.log("I will add the results of the sub-problems back together to get {}.".format(latex_wrap(combined.latex())))
    return combined
  elif expr.is_a(Product):
    logger.log("{} is a product. I will solve the two sub-problems and then multiply the results.".format(latex_wrap(expr.latex())))
    subproblem_a, subproblem_b = logger.split('subproblem-a', 'subproblem-b')
    sub_a = attempt_integral(expr.a, subproblem_a)
    sub_b = attempt_integral(expr.b, subproblem_b)
    combined = Product(sub_a, sub_b)
    logger.log("I will multiply the results of the sub-problems back together to get {}.".format(latex_wrap(combined.latex())))
    return combined

  # if the expression has any other form, then it's probably a basic element, so it's already simplified.
  else:
    logger.log("{} is already simplified.".format(latex_wrap(expr.latex())))
    return expr


if __name__ == "__main__":
  """
  Run the solver from the command line.
  Prompt for an expression and integrate that or a default
  if an input is not provided.
  """
  default = "int 3 x / 4 dx"
  input_str = raw_input(
    "Enter a string to be integrated.\n"
    "Just press enter to integrate '{}'\n"
    "-> ".format(default))
  input_str = input_str if input_str != "" else default
  log = SubLogger('root')
  attempt_integral(parse(input_str), log)
  for msg in log.entries:
    print msg
