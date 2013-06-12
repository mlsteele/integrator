from test_frame import *
from elements import *

def test_Expression():
  try:
    Expression()
  except:
    pass
  else:
    assert_equal('abstract class', 'instantiable')


def test_Number():
  n1 = Number(3)
  assert_equal(n1.n, 3)

  n2 = Number(3.0)
  assert_equal(n2.n, n2.simplified().n)

  n3 = Number(3 / 5)
  assert_equal(n3.n, n3.simplified().n)

  n4 = Number(3 / 5.)
  assert_equal(n4.n, n4.simplified().n)


def test_Variable():
  vset = VariableSet()
  v1 = vset.variable('x')
  assert_equal(v1.symbol(), 'x')
  assert_equal(v1.simplified().symbol(), 'x')
  assert_equal(v1.simplified(), v1)


def test_VariableSet():
  vset = VariableSet()
  va = vset.variable('a')
  vb = vset.variable('b')
  vuk = vset.variable()
  assert_equal(VariableSet.MAX_VARIABLES > 3, True)
  vs = [vset.variable() for _ in range(VariableSet.MAX_VARIABLES - 3)]
  assert_equal(va.symbol(), 'a')
  assert_equal(vb.symbol(), 'b')
  symbols = ['a', 'b', vuk.symbol()] + [v.symbol() for v in vs]
  assert_equal(len(set(symbols)), len(symbols))


def test_Sum():
  x = Number(3)
  y = Number(6)
  s = Sum(x,y)
  assert_equal(s.simplified().n, 9)
  assert_equal(x.n, 3)
  assert_equal(y.n, 6)

  vset = VariableSet()
  x = vset.variable('x')
  y = Number(6)
  s = Sum(x,y)
  assert_equal(s.simplified().a.symbol(), 'x')
  assert_equal(s.simplified().b.n, 6)

  x = Sum(Number(4), Number(3))
  y = Number(6)
  s = Sum(x,y)
  assert_equal(s.simplified().n, 13)


def test_Product():
  x = Number(3)
  y = Number(6)
  s = Product(x,y)
  assert_equal(s.simplified().n, 18)
  assert_equal(x.n, 3)
  assert_equal(y.n, 6)

  vset = VariableSet()
  x = vset.variable('x')
  y = Number(6)
  s = Product(x,y)
  assert_equal(s.simplified().a.symbol(), 'x')
  assert_equal(s.simplified().b.n, 6)


def test_Fraction():
  x = Number(3)
  y = Number(6)
  s = Fraction(x,y)
  assert_equal(isinstance(s.simplified(), Fraction), True)
  assert_equal(s.simplified().numr, 1)
  assert_equal(s.simplified().denr, 2)
  assert_equal(x.n, 3)
  assert_equal(y.n, 6)

  vset = VariableSet()
  x = vset.variable()
  y = Sum(Product(Number(3), Number(5)), Number(2))
  s = Fraction(x,y)
  assert_equal(isinstance(s.simplified(), Fraction), True)
  assert_equal(isinstance(s.simplified().numr, Variable), True)
  assert_equal(isinstance(s.simplified().denr, Number), True)
  assert_equal(s.simplified().denr.n, 17)

  vset = VariableSet()
  x = Sum(Product(Number(3), Number(5)), Number(2))
  y = vset.variable()
  s = Fraction(x,y)
  assert_equal(isinstance(s.simplified(), Fraction), True)
  assert_equal(isinstance(s.simplified().denr, Variable), True)
  assert_equal(isinstance(s.simplified().numr, Number), True)
  assert_equal(s.simplified().numr.n, 17)

  vset = VariableSet()
  x = vset.variable()
  y = Number(1)
  s = Fraction(x,y)
  assert_equal(isinstance(s.simplified(), Variable), True)
  assert_equal(s.simplified().symbol(), x.symbol())
  assert_equal(s.simplified(), x)


def test_Integral():
  exp = Number(5)
  intg = Integral(exp, 'x')
  assert_equal(intg.exp.n, 5)
  assert_equal(intg.var.symbol(), 'x')

  exp = Sum(Number(5), Number(3))
  intg = Integral(exp, 'y')
  assert_equal(intg.simplify().exp.n, 8)
  assert_equal(intg.simplify().var.symbol(), 'y')


def test_Power():
  b = Number(5)
  e = Number(3)
  p = Power(b, e)
  assert_equal(p.base.n, 5)
  assert_equal(p.exponent.n, 3)
  assert_equal(p.simplified().n, 125)

  b = Sum(Number(5), Number(3.5))
  e = Number(3)
  p = Power(b, e)
  assert_equal(p.base.simplified().n, 8.5)
  assert_equal(p.exponent.n, 3)
  assert_equal(p.simplified().n, 614.125)


def test_Equality():
  x = Number(2)
  y = Number(2)
  assert_equal(x, x)
  assert_equal(x == y, True)
  assert_equal(x != y, False)

  vset = VariableSet()
  x = Product(Number(2), vset.variable('b'))
  y = Product(Number(2), vset.variable('b'))
  assert_equal(x, y)

  vset = VariableSet()
  x = Product(Number(2), vset.variable('b'))
  y = Product(Number(2), vset.variable('c'))
  assert_equal(x != y, True)

  vset = VariableSet()
  x = Product(Number(2), vset.variable('b'))
  y = Product(Number(2), vset.variable('c'))
  assert_bool(false= x == y)
  assert_bool(true= x != y)

  vset = VariableSet()
  x = Product(Number(3), vset.variable('b'))
  y = Product(Number(2), vset.variable('b'))
  assert_bool(false= x == y)
  assert_bool(true= x != y)

  from parser import parse

  vset = VariableSet()
  x = parse("3x + 2", vset)
  y = parse("3x + 2", vset)
  assert_bool(true= x == y, false= x != y)

  vset = VariableSet()
  x = parse("3x * 2", vset)
  y = parse("3x * 3", vset)
  assert_bool(false= x == y, true= x != y)


if __name__ == "__main__":
  do_test(test_Expression,  "Expression")
  do_test(test_Number,      "Number")
  do_test(test_Variable,    "Variable")
  do_test(test_VariableSet, "VariableSet")
  do_test(test_Sum,         "Sum")
  do_test(test_Product,     "Product")
  do_test(test_Fraction,    "Fraction")
  do_test(test_Power,       "Power")
  do_test(test_Equality,    "Equality")
