from elements import *

class IntegrationStrategy(object):
  def __init__(self):
    raise "Strategy is an abstract class"

  def apply(exp):
    raise "apply not implemented"


# int 4 dx = 4x + C
class Constant(IntegrationStrategy):
  @classmethod
  def applicable(self, intg):
    exp = intg.simplified().exp
    return isinstance(exp, Number) and isinstance(intg.simplified().exp, Number)

  @classmethod
  def apply(self, intg):
    return Product(intg.exp, intg.var)


# int 4x dx = 4 * int x dx
class ConstantFactor(IntegrationStrategy):
  @classmethod
  def applicable(self, intg):
    exp = intg.simplified().exp
    return isinstance(exp, Product) and (isinstance(exp.a, Number) or isinstance(exp.b, Number))

  @classmethod
  def apply(self, intg):
    exp = intg.simplified().exp
    integrand, constant_factor = sorted([exp.a, exp.b], key=lambda e: isinstance(e, Number))
    return Product(constant_factor, Integral(integrand, intg.var))


# int x^3 dx = 1/4 x^4 + C
class NumberExponent(IntegrationStrategy):
  @classmethod
  def applicable(self, intg):
    expr = intg.simplified().exp
    return isinstance(expr, Power) and isinstance(expr.base, Variable) and (expr.base.symbol == intg.var.symbol) and isinstance(expr.exponent, Number)

  @classmethod
  def apply(self, intg):
    expr = intg.simplified().exp
    # TODO do not use floating point reciprocal!!!
    recip_n = Number(1 / float(expr.exponent.n))
    n_plus_one = Sum(expr.exponent, Number(1))
    return Product(recip_n, Power(intg.var, n_plus_one))


# int x + x^2 dx = int x dx + int x^2 dx
class DistributeAddition(IntegrationStrategy):
  @classmethod
  def applicable(self, intg):
    exp = intg.simplified().exp
    return isinstance(expr, Sum)

  @classmethod
  def apply(self, intg):
    exp = intg.simplified().exp
    return Sum(Integral(exp.a, intg.var), Integral(exp.b, intg.var))
