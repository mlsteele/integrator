import string

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


# unique set of variables
class VariableSet(object):
  SYMBOLS = set(string.letters)
  MAX_VARIABLES = len(SYMBOLS)

  def __init__(self):
    self.lookup = {}

  def new_variable(self, symbol=None):
    if symbol == None:
      symbol = self.unused_symbol()
    if not symbol in self.SYMBOLS:
      raise ValueError('symbol "' + str(symbol) + '" not in SYMBOLS')
    elif symbol in self.lookup.keys():
      raise ValueError('symbol "' + str(symbol) + '" already used in VariableSet')

    v = Variable(self)
    self.lookup[v] = symbol
    return v

  def variable(self, symbol=None):
    if symbol == None:
      return self.new_variable()
    elif not symbol in self.SYMBOLS:
      raise ValueError('symbol "' + symbol + '" not in SYMBOLS')
    elif symbol in map(lambda (var, sym): sym, self.lookup.items()):
      return filter(lambda (var, sym): sym == symbol, self.lookup.items())[0][0]
    else:
      return self.new_variable(symbol)

  def unused_symbol(self):
    used = set(map(lambda (var, sym): sym, self.lookup.items()))
    unused = self.SYMBOLS - used
    if len(unused) == 0:
      raise Exception("VariableSet out of symbols")
    return unused.pop()

  def symbol_for(self, var):
    return self.lookup[var]


# do not instantiate this class, use variableset.variable(optional_symbol)
class Variable(Expression):
  def __init__(self, vset):
    if not isinstance(vset, VariableSet):
      raise Exception('Variable instantiated without VariableSet')
    self.vset = vset

  def symbol(self):
    return self.vset.symbol_for(self)

  def __repr__(self):
    return self.symbol()


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
    return "(%s ^ %s)" %(self.base, self.exponent)


class Integral(Expression):
  def __init__(self, exp, var):
    self.exp = exp
    self.var = var

  def simplified(self):
    return Integral(self.exp.simplified(), self.var)

  def __repr__(self):
    return "int[%s]d%s" %(self.exp, self.var)
