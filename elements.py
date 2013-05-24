class Expression(object):
  def __init__(self):
    raise Exception("Expression is an abstract class")

  def simplified(self):
    return self

  def latex(self):
    raise Exception("latex not implemented for %s" % self)


class Number(Expression):
  def __init__(self, n):
    self.n = n

  def __repr__(self):
    return str(self.n)


# class Fraction(Expression):
#   def __init__(self, numerator, denominator):
#     self.numerator   = numerator
#     self.denominator = numerator


class Variable(Expression):
  def __init__(self, symbol):
    self.symbol = symbol

  def __repr__(self):
    return self.symbol


class Sum(Expression):
  def __init__(self, a, b):
    self.a = a
    self.b = b

  def simplified(self):
    if isinstance(self.a, Number) and isinstance(self.b, Number):
      return Number(self.a.n + self.b.n)
    else:
      return Sum(self.a.simplified(), self.b.simplified())

  def __repr__(self):
    return "(%s + %s)" %(self.a, self.b)


class Product(Expression):
  def __init__(self, a, b):
    self.a = a
    self.b = b

  def simplified(self):
    if isinstance(self.a, Number) and isinstance(self.b, Number):
      return Number(self.a.n * self.b.n)
    else:
      return Product(self.a.simplified(), self.b.simplified())

  def __repr__(self):
    return "(%s * %s)" %(self.a, self.b)


class Integral(Expression):
  def __init__(self, exp, var):
    self.exp = exp
    self.var = var

  def simplified(self):
    return Integral(self.exp.simplified(), self.var)

  def __repr__(self):
    return "int[%s]d%s" %(self.exp, self.var.symbol)
