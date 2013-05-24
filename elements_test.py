from elements import *

def assert_equal(a,b):
  if a != b:
    errstr = "ASSERT FAILED: %s != %s" %(a,b)
    raise Exception(errstr)
  return True

def do_test(test, name):
  print "test passed: %s" %name

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
  v1 = Variable('x')
  assert_equal(v1.symbol, 'x')
  assert_equal(v1.simplified().symbol, 'x')

def test_Sum():
  x = Number(3)
  y = Number(6)
  s = Sum(x,y)
  assert_equal(s.simplified.n, 9)
  assert_equal(x.n, 3)
  assert_equal(y.n, 6)

  x = Variable('x')
  y = Number(6)
  s = Sum(x,y)
  assert_equal(s.simplified().a.symbol, 'x')
  assert_equal(s.simplified().b.n, '6')

def test_Product():
  x = Number(3)
  y = Number(6)
  s = Product(x,y)
  assert_equal(s.simplified.n, 18)
  assert_equal(x.n, 3)
  assert_equal(y.n, 6)

  x = Variable('x')
  y = Number(6)
  s = Product(x,y)
  assert_equal(s.simplified().a.symbol, 'x')
  assert_equal(s.simplified().b.n, '6')

def test_Integral():
  exp = Number(5)
  intg = Integral(exp, 'x')
  assert_equal(intg.exp.n, 5)
  assert_equal(intg.var.symbol, 'x')

  exp = Sum(Number(5), Number(3))
  intg = Integral(exp, 'y')
  assert_equal(intg.simplify().exp.n, 8)
  assert_equal(intg.simplify().var.symbol, 'y')

if __name__ == "__main__":
  do_test(test_Expression, "Expression")
  do_test(test_Number,     "Number")
  do_test(test_Variable,   "Variable")
  do_test(test_Sum,        "Sum")
  do_test(test_Product,    "Product")
  do_test(test_Integral,   "Integral")
