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
    a = self.a.simplified()
    b = self.b.simplified()
    if isinstance(a, Number) and isinstance(b, Number):
      return Number(a.n + b.n)
    else:
      return Sum(a, b)

  def __repr__(self):
    return "(%s + %s)" %(self.a, self.b)


class Product(Expression):
  def __init__(self, a, b):
    self.a = a
    self.b = b

  def simplified(self):
    a = self.a.simplified()
    b = self.b.simplified()
    if isinstance(a, Number) and isinstance(b, Number):
      return Number(a.n * b.n)
    else:
      return Product(a, b)

  def __repr__(self):
    return "(%s * %s)" %(self.a, self.b)


class Power(Expression):
  def __init__(self, base, exponent):
    self.base     = base
    self.exponent = exponent

  def simplified(self):
    base     = self.base.simplified()
    exponent = self.exponent.simplified()
    if isinstance(base, Number) and isinstance(exponent, Number):
      return Number(base.n ** exponent.n)
    else:
      return Power(base.simplified(), exponent.simplified())

  def __repr__(self):
    return "(%s ^ %s)" %(self.a, self.b)


class Integral(Expression):
  def __init__(self, exp, var):
    self.exp = exp
    self.var = var

  def simplified(self):
    return Integral(self.exp.simplified(), self.var)

  def __repr__(self):
    return "int[%s]d%s" %(self.exp, self.var.symbol)
