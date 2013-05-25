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
  v1 = vset.new_variable('x')
  assert_equal(v1.symbol(), 'x')
  assert_equal(v1.simplified().symbol(), 'x')
  assert_equal(v1.simplified(), v1)


def test_Sum():
  x = Number(3)
  y = Number(6)
  s = Sum(x,y)
  assert_equal(s.simplified().n, 9)
  assert_equal(x.n, 3)
  assert_equal(y.n, 6)

  vset = VariableSet()
  x = vset.new_variable('x')
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
  x = vset.new_variable('x')
  y = Number(6)
  s = Product(x,y)
  assert_equal(s.simplified().a.symbol(), 'x')
  assert_equal(s.simplified().b.n, 6)


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

if __name__ == "__main__":
  do_test(test_Expression, "Expression")
  do_test(test_Number,     "Number")
  do_test(test_Variable,   "Variable")
  do_test(test_Sum,        "Sum")
  do_test(test_Product,    "Product")
  do_test(test_Power,      "Power")
