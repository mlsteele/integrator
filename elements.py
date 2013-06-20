import string
from fractions import gcd

# TODO make Expression the owner of a VariableSet
class Expression(object):
  def __init__(self):
    raise Exception("Expression is an abstract class")

  def reciprocal(self):
    return Fraction(Number(1), self)

  def simplified(self):
    return self

  # TODO figure out how this should interact with different variablesets
  # TODO consider alternate forms (simplify before test?)
  def __eq__(self, other):
    return self.__repr__() == other.__repr__()

  def __ne__(self, other):
    return not self.__eq__(other)

  def latex(self):
    raise Exception("latex not implemented for %s" % self)


class Number(Expression):
  def __init__(self, n):
    self.n = n

  def __repr__(self):
    return "{!r}".format(self.n)

  def latex(self):
    return "{!r}".format(self.n)

# unique set of variables
class VariableSet(object):
  SYMBOLS = set(string.letters)
  MAX_VARIABLES = len(SYMBOLS)

  def __init__(self):
    self.lookup = {} # hash of {Variable instance: symbol string}`

  # fetch or create a variable with symbol=symbol
  # if symbol=None then create a new variable
  def variable(self, symbol=None):
    if symbol == None:
      return self.new_variable()
    else:
      existing = self.variable_for(symbol)
      if existing != None:
        return existing
      else:
        return self.new_variable(symbol=symbol)

  # force creation of new variable
  # only one of symbol or suggest is allowed
  # if symbol then new variable will be created with symbol=symbol
  # if suggest then a new variable will be created, and if possible it will have symbol=suggest
  def new_variable(self, symbol=None, suggest=None):
    if symbol != None and suggest != None:
      return ValueError('only one of symbol and suggest is allowed, both supplied (symbol=%s, suggest=%s)' %(symbol, suggest))
    elif symbol != None:
      return self._new_variable(symbol)
    elif suggest != None:
      if self.variable_for(suggest) == None:
        return self._new_variable(suggest)
      else:
        return self._new_variable()
    else:
      return self._new_variable()

  # create a new variable with an unused symbol
  def _new_variable(self, symbol=None):
    if symbol != None:
      self._check_symbol_valid_new(symbol)
    else:
      symbol = self._unused_symbol()

    v = Variable(self)
    self.lookup[v] = symbol
    return v

  # throws ValueError on invalid symbol
  def _check_symbol_valid(self, symbol):
    if symbol == None:
      raise ValueError("symbol of None is not allowed")
    elif not symbol in self.SYMBOLS:
      raise ValueError("symbol '%s' not in SYMBOLS" % str(symbol) )

  # throws ValueError on invalid or used symbol
  def _check_symbol_valid_new(self, symbol):
    self._check_symbol_valid(symbol)
    if self.variable_for(symbol) != None:
      raise ValueError("symbol '%s' already used in VariableSet" % str(symbol) )

  def _unused_symbol(self):
    used = set(map(lambda (var, sym): sym, self.lookup.items()))
    unused = self.SYMBOLS - used
    if len(unused) == 0:
      raise Exception("VariableSet out of symbols")
    return unused.pop()

  def symbol_for(self, var):
    return self.lookup[var]

  # use self.lookup to backwards-lookup the Variable from the symbol
  # return None if no variables exist for symbol
  def variable_for(self, symbol):
    filtered = filter(lambda (var, sym): sym == symbol, self.lookup.items())

    if len(filtered) == 0:
      return None
    elif len(filtered) == 1:
      return filtered[0][0]
    else:
      raise RuntimeError("more than one variable points to same symbol! (symbol=%s)" %symbol)


# do not instantiate this class, use variableset.variable(symbol=optional_symbol)
class Variable(Expression):
  def __init__(self, vset):
    if not isinstance(vset, VariableSet):
      raise Exception('Variable instantiated without VariableSet')
    self.vset = vset

  def symbol(self):
    return self.vset.symbol_for(self)

  def __repr__(self):
    return "{0}".format(self.symbol())

  def latex(self):
    return "{0}".format(self.symbol())

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

  def latex(self):
    return "(%s + %s)" %(self.a.latex(), self.b.latex())


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

  def latex(self):
    return "%s \cdot %s" %(self.a.latex(), self.b.latex())


class Fraction(Expression):
  def __init__(self, numr, denr):
    self.numr = numr
    self.denr = denr

  def reciprocal(self):
    return Fraction(self.denr, self.numr)

  def simplified(self):
    numr = self.numr.simplified()
    denr = self.denr.simplified()

    if isinstance(numr, Number) and isinstance(denr, Number):
      gcd_ = gcd(numr.n, denr.n)
      numr = Number(numr.n / gcd_)
      denr = Number(denr.n / gcd_)

    if isinstance(denr, Number) and denr.n == 1:
      return numr
    else:
      return Fraction(numr, denr)

  def __repr__(self):
    return "(%s / %s)" %(self.numr, self.denr)

  def latex(self):
    return "\\frac{%s}{%s}" %(self.numr.latex(), self.denr.latex())

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

  def latex(self) :
    return "{%s}^{%s}" %(self.base.latex(), self.exponent.latex())

class Logarithm(Expression):
  def __init__(self, arg, base="euler"):
    self.arg = arg
    self.base = base

  def simplified(self):
    return Logarithm(self.arg.simplified(), self.base)

  def __repr__(self):
    if self.base == "euler" :
      return "log(%s)" %(self.arg)
    else :
      return "log_(%s) %s" %(self.arg, self.base)
    
  def latex(self):
    if self.base == "euler" :
      return "\log{%s}" %(self.arg.latex())
    else :
      return "log_{%s}{%s}" %(self.arg.latex(), self.base.latex())

class Integral(Expression):
  def __init__(self, exp, var):
    self.exp = exp
    self.var = var

  def simplified(self):
    return Integral(self.exp.simplified(), self.var)

  def __repr__(self):
    return "int[%s]d%s" %(self.exp, self.var)

  def latex(self):
    return "\\int{%s}\;d%s" %(self.exp.latex(), self.var.latex())
