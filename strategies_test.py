from test_frame import *
from elements import *
from strategies import *

def test_IntegrationStrategy():
  try:
    IntegrationStrategy()
  except:
    pass
  else:
    assert_equal('abstract class', 'instantiable')


def test_ConstantTerm():
  vset = VariableSet()
  var = vset.new_variable()
  exp = Number(4)
  intg = Integral(exp, var)
  assert_equal(ConstantTerm.applicable(intg), True)
  res = ConstantTerm.apply(intg)
  assert_equal(res.a.a.n, 4)
  assert_equal(res.a.b, intg.var)
  assert_equal(isinstance(res.b, Variable), True)

  vset = VariableSet()
  var = vset.new_variable()
  exp = Product(Number(3), Number(4))
  intg = Integral(exp, var)
  assert_equal(ConstantTerm.applicable(intg), True)
  res = ConstantTerm.apply(intg).simplified()
  assert_equal(res.a.a.n, 12)
  assert_equal(res.a.b, intg.var)
  assert_equal(isinstance(res.b, Variable), True)

  vset = VariableSet()
  var = vset.new_variable()
  exp = Product(vset.new_variable(), Number(4))
  intg = Integral(exp, var)
  assert_equal(ConstantTerm.applicable(intg), False)


def test_DistributeAddition():
  vset = VariableSet()
  var = vset.new_variable()
  exp = Sum(Number(4), vset.new_variable('y'))
  intg = Integral(exp, var)
  assert_equal(DistributeAddition.applicable(intg), True)
  res = DistributeAddition.apply(intg)
  assert_equal(isinstance(res, Sum), True)
  assert_equal(res.a.exp.n, 4)
  assert_equal(res.a.var.symbol(), 'A')
  assert_equal(res.b.exp.symbol(), 'y')
  assert_equal(res.b.var.symbol(), 'A')


def test_NumberExponent():
  vset = VariableSet()
  var = vset.new_variable()
  var2 = vset.new_variable()
  exp = Power(var, Number(2))
  intg = Integral(exp, var2)
  assert_equal(NumberExponent.applicable(intg), False)

  vset = VariableSet()
  var = vset.new_variable()
  exp = Power(var, Number(2))
  intg = Integral(exp, var)
  assert_equal(NumberExponent.applicable(intg), True)
  res = NumberExponent.apply(intg).simplified()
  assert_equal(isinstance(res, Product), True)
  assert_equal(res.a.n, 1 / 3.) # TODO remove floating point division
  assert_equal(res.b.base, var)
  assert_equal(res.b.exponent.n, 3)


if __name__ == "__main__":
  do_test(test_IntegrationStrategy, "IntegrationStrategy")
  do_test(test_ConstantTerm,        "ConstantTerm")
  do_test(test_DistributeAddition,  "DistributeAddition")
  do_test(test_NumberExponent,      "NumberExponent")
