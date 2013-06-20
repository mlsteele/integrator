from elements import *

# add on integration uncertainty variable
def add_integration_constant(expr, original_intg):
  return Sum(expr, original_intg.var.vset.new_variable(suggest='C'))


# returns true if the expression is a constant with respect to the variable
def is_constant(expr, var) :
  if isinstance(expr, Number) :
    return True
  elif isinstance(expr, Variable) :
    return (expr != var)
  elif isinstance(expr, Sum) or isinstance(expr, Product):
    return is_constant(expr.a, var) and is_constant(expr.b, var)
  elif isinstance(expr, Fraction):
    return is_constant(expr.numr, var) and is_constant(expr.denr, var)
  else :
    return False


class IntegrationStrategy(object):
  def __init__(self):
    raise "Strategy is an abstract class"

  def apply(exp):
    raise "apply not implemented"


# int 4 dx = 4x + C
class ConstantTerm(IntegrationStrategy):
  description = "integral of a constant term"

  @classmethod
  def applicable(self, intg):
    return is_constant(intg.exp, intg.var)

  @classmethod
  def apply(self, intg):
    exp = intg.exp.simplified()
    return add_integration_constant(Product(exp, intg.var), intg)


# int 4x dx = 4 * int x dx
class ConstantFactor(IntegrationStrategy):
  description = "integral with a constant factor"

  @classmethod
  def applicable(self, intg):
    exp = intg.simplified().exp
    return isinstance(exp, Product) and is_constant(exp.a, intg.var) or is_constant(exp.b, intg.var)

  @classmethod
  def apply(self, intg):
    exp = intg.simplified().exp
    integrand, constant_factor = sorted([exp.a, exp.b], key=lambda e: is_constant(e, intg.var) )
    return Product(constant_factor, Integral(integrand, intg.var))


# int x dx = 1/2 x^2 + C
class SimpleIntegral(IntegrationStrategy):
  description = "integral of the integration variable occuring by itself."

  @classmethod
  def applicable(self, intg):
    expr = intg.simplified().exp
    return isinstance(expr, Variable) and (expr is intg.var)

  @classmethod
  def apply(self, intg):
    expr = intg.simplified().exp
    half = Fraction(Number(1), Number(2))
    new_expr = Product(half, Power(expr, Number(2)))
    return add_integration_constant(new_expr, intg)


# int x^3 dx = 1/4 x^4 + C
class NumberExponent(IntegrationStrategy):
  description = "integral with a numerical exponent"

  @classmethod
  def applicable(self, intg):
    expr = intg.simplified().exp
    return isinstance(expr, Power) and isinstance(expr.base, Variable) and (expr.base.symbol == intg.var.symbol) and isinstance(expr.exponent, Number)

  @classmethod
  def apply(self, intg):
    expr = intg.simplified().exp
    # TODO do not use floating point reciprocal!!!
    n_plus_one = Sum(expr.exponent, Number(1)).simplified()
    recip_n = n_plus_one.reciprocal()
    new_expr = Product(recip_n, Power(intg.var, n_plus_one))
    return add_integration_constant(new_expr, intg)


# int x + x^2 dx = int x dx + int x^2 dx
class DistributeAddition(IntegrationStrategy):
  description = "integral of sums to sum of integrals"

  @classmethod
  def applicable(self, intg):
    exp = intg.simplified().exp
    return isinstance(exp, Sum)

  @classmethod
  def apply(self, intg):
    exp = intg.simplified().exp
    new_expr = Sum(Integral(exp.a, intg.var), Integral(exp.b, intg.var))
    return add_integration_constant(new_expr, intg)

# class OneOverX(IntegrationStrategy):
#   description = "The integral of 1/x is ln(x)."
  
#   @classmethod
#   def applicable(self, intg):
#     exp = intg.simplified().exp
#     return isInstance(exp, Fraction)

STRATEGIES = [ConstantTerm, ConstantFactor, SimpleIntegral, NumberExponent, DistributeAddition]
