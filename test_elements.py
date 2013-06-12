import unittest

from elements import *

class TestElements(unittest.TestCase):
  def test_Expression(self):
    try:
      Expression()
    except:
      pass
    else:
      self.assertEqual('abstract class', 'instantiable')


  def test_Number(self):
    n1 = Number(3)
    self.assertEqual(n1.n, 3)

    n2 = Number(3.0)
    self.assertEqual(n2.n, n2.simplified().n)

    n3 = Number(3 / 5)
    self.assertEqual(n3.n, n3.simplified().n)

    n4 = Number(3 / 5.)
    self.assertEqual(n4.n, n4.simplified().n)


  def test_Variable(self):
    vset = VariableSet()
    v1 = vset.variable('x')
    self.assertEqual(v1.symbol(), 'x')
    self.assertEqual(v1.simplified().symbol(), 'x')
    self.assertEqual(v1.simplified(), v1)


  def test_VariableSet(self):
    vset = VariableSet()
    va = vset.variable('a')
    vb = vset.variable('b')
    vuk = vset.variable()
    self.assertEqual(VariableSet.MAX_VARIABLES > 3, True)
    vs = [vset.variable() for _ in range(VariableSet.MAX_VARIABLES - 3)]
    self.assertEqual(va.symbol(), 'a')
    self.assertEqual(vb.symbol(), 'b')
    symbols = ['a', 'b', vuk.symbol()] + [v.symbol() for v in vs]
    self.assertEqual(len(set(symbols)), len(symbols))


  def test_Sum(self):
    x = Number(3)
    y = Number(6)
    s = Sum(x,y)
    self.assertEqual(s.simplified().n, 9)
    self.assertEqual(x.n, 3)
    self.assertEqual(y.n, 6)

    vset = VariableSet()
    x = vset.variable('x')
    y = Number(6)
    s = Sum(x,y)
    self.assertEqual(s.simplified().a.symbol(), 'x')
    self.assertEqual(s.simplified().b.n, 6)

    x = Sum(Number(4), Number(3))
    y = Number(6)
    s = Sum(x,y)
    self.assertEqual(s.simplified().n, 13)


  def test_Product(self):
    x = Number(3)
    y = Number(6)
    s = Product(x,y)
    self.assertEqual(s.simplified().n, 18)
    self.assertEqual(x.n, 3)
    self.assertEqual(y.n, 6)

    vset = VariableSet()
    x = vset.variable('x')
    y = Number(6)
    s = Product(x,y)
    self.assertEqual(s.simplified().a.symbol(), 'x')
    self.assertEqual(s.simplified().b.n, 6)


  def test_Fraction(self):
    x = Number(3)
    y = Number(6)
    s = Fraction(x,y)
    self.assertEqual(isinstance(s.simplified(), Fraction), True)
    self.assertEqual(s.simplified().numr, 1)
    self.assertEqual(s.simplified().denr, 2)
    self.assertEqual(x.n, 3)
    self.assertEqual(y.n, 6)

    vset = VariableSet()
    x = vset.variable()
    y = Sum(Product(Number(3), Number(5)), Number(2))
    s = Fraction(x,y)
    self.assertEqual(isinstance(s.simplified(), Fraction), True)
    self.assertEqual(isinstance(s.simplified().numr, Variable), True)
    self.assertEqual(isinstance(s.simplified().denr, Number), True)
    self.assertEqual(s.simplified().denr.n, 17)

    vset = VariableSet()
    x = Sum(Product(Number(3), Number(5)), Number(2))
    y = vset.variable()
    s = Fraction(x,y)
    self.assertEqual(isinstance(s.simplified(), Fraction), True)
    self.assertEqual(isinstance(s.simplified().denr, Variable), True)
    self.assertEqual(isinstance(s.simplified().numr, Number), True)
    self.assertEqual(s.simplified().numr.n, 17)

    vset = VariableSet()
    x = Number(6)
    y = Number(3)
    s = Fraction(x,y)
    self.assertEqual(isinstance(s.simplified(), Number), True)
    self.assertEqual(s.simplified().n, 2)

    vset = VariableSet()
    x = vset.variable()
    y = Number(1)
    s = Fraction(x,y)
    self.assertEqual(isinstance(s.simplified(), Variable), True)
    self.assertEqual(s.simplified().symbol(), x.symbol())
    self.assertEqual(s.simplified(), x)


  def test_Integral(self):
    exp = Number(5)
    vset = VariableSet()
    x1 = vset.variable('x')
    intg = Integral(exp, x1)
    self.assertEqual(intg.exp.n, 5)
    self.assertEqual(intg.var.symbol(), 'x')

    exp = Sum(Number(5), Number(3))
    vset = VariableSet()
    y1 = vset.variable('y')
    intg = Integral(exp, y1)
    self.assertEqual(intg.simplified().exp.n, 8)
    self.assertEqual(intg.simplified().var.symbol(), 'y')

  def test_Power(self):
    b = Number(5)
    e = Number(3)
    p = Power(b, e)
    self.assertEqual(p.base.n, 5)
    self.assertEqual(p.exponent.n, 3)
    self.assertEqual(p.simplified().n, 125)

    b = Sum(Number(5), Number(3.5))
    e = Number(3)
    p = Power(b, e)
    self.assertEqual(p.base.simplified().n, 8.5)
    self.assertEqual(p.exponent.n, 3)
    self.assertEqual(p.simplified().n, 614.125)


  def test_Equality(self):
    x = Number(2)
    y = Number(2)
    self.assertEqual(x, x)
    self.assertEqual(x == y, True)
    self.assertEqual(x != y, False)

    vset = VariableSet()
    x = Product(Number(2), vset.variable('b'))
    y = Product(Number(2), vset.variable('b'))
    self.assertEqual(x, y)

    vset = VariableSet()
    x = Product(Number(2), vset.variable('b'))
    y = Product(Number(2), vset.variable('c'))
    self.assertEqual(x != y, True)

    vset = VariableSet()
    x = Product(Number(2), vset.variable('b'))
    y = Product(Number(2), vset.variable('c'))
    self.assertFalse(x == y)
    self.assertTrue(x != y)

    vset = VariableSet()
    x = Product(Number(3), vset.variable('b'))
    y = Product(Number(2), vset.variable('b'))
    self.assertFalse(x == y)
    self.assertTrue(x != y)

    from parser import parse

    vset = VariableSet()
    x = parse("3x + 2", vset)
    y = parse("3x + 2", vset)
    self.assertTrue(x == y)
    self.assertFalse(x != y)

    vset = VariableSet()
    x = parse("3x * 2", vset)
    y = parse("3x * 3", vset)
    self.assertTrue(x != y)
    self.assertFalse(x == y)


if __name__ == '__main__':
  unittest.main()
