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


if __name__ == "__main__":
  do_test(test_IntegrationStrategy, "IntegrationStrategy")
  do_test(test_ConstantTerm, "ConstantTerm")
