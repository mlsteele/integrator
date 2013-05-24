from elements import *
from strategies import *

if __name__ == "__main__":
  four = Number(4)
  fourplusfive = Sum(Number(4), Number(5))
  fourtimesfive = Product(Number(4), Number(5))
  fourtimesx = Product(Variable('x'), Number(5))
  print fourtimesfive.simplified()

  intg1 = Integral(fourtimesfive, Variable('x'))

  print intg1
  print ConstantFactor.applicable(intg1)
  # print ConstantFactor.apply(intg1)
