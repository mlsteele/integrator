import unittest

from elements import *
from strategies import *

class TestStrategies(unittest.TestCase):

  def test_IntegrationStrategy(self):
    try:
      IntegrationStrategy()
    except:
      pass
    else:
      self.assertEqual('abstract class', 'instantiable')


  def test_ConstantTerm(self):
    vset = VariableSet()
    var = vset.variable()
    exp = Number(4)
    intg = Integral(exp, var)
    self.assertEqual(ConstantTerm.applicable(intg), True)
    res = ConstantTerm.apply(intg)
    self.assertEqual(res.a.a.n, 4)
    self.assertEqual(res.a.b, intg.var)
    self.assertEqual(isinstance(res.b, Variable), True)

    vset = VariableSet()
    var = vset.variable()
    exp = Product(Number(3), Number(4))
    intg = Integral(exp, var)
    self.assertEqual(ConstantTerm.applicable(intg), True)
    res = ConstantTerm.apply(intg).simplified()
    self.assertEqual(res.a.a.n, 12)
    self.assertEqual(res.a.b, intg.var)
    self.assertEqual(isinstance(res.b, Variable), True)

    vset = VariableSet()
    var = vset.variable()
    exp = Product(vset.variable(), Number(4))
    intg = Integral(exp, var)
    self.assertEqual(ConstantTerm.applicable(intg), False)


  def test_DistributeAddition(self):
    vset = VariableSet()
    var = vset.variable()
    exp = Sum(Number(4), vset.variable('y'))
    intg = Integral(exp, var)
    self.assertEqual(DistributeAddition.applicable(intg), True)
    res = DistributeAddition.apply(intg)
    self.assertEqual(isinstance(res, Sum), True)
    self.assertEqual(res.a.a.exp.n, 4)
    self.assertEqual(res.a.a.var.symbol(), 'A')
    self.assertEqual(res.a.b.exp.symbol(), 'y')
    self.assertEqual(res.a.b.var.symbol(), 'A')


  def test_ConstantPower(self):
    vset = VariableSet()
    var = vset.variable()
    var2 = vset.variable()
    exp = Power(var, Number(2))
    intg = Integral(exp, var2)
    self.assertEqual(ConstantPower.applicable(intg), False)

    vset = VariableSet()
    var = vset.variable()
    exp = Power(var, Number(2))
    intg = Integral(exp, var)
    self.assertEqual(ConstantPower.applicable(intg), True)
    res = ConstantPower.apply(intg).simplified()
    self.assertEqual(isinstance(res.a, Product), True)
    self.assertEqual(isinstance(res.a.a, Fraction), True)
    self.assertEqual(res.a.a.numr, 1)
    self.assertEqual(res.a.a.denr, 3)
    self.assertEqual(res.a.b.base, var)
    self.assertEqual(res.a.b.exponent.n, 3)


if __name__ == "__main__":
  unittest.main()
