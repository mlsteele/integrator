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


# int (x + x^2) dx == int (x) + int (x^2) dx
# class Linearity(IntegrationStrategy):
