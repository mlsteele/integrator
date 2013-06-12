from test_frame import *
from parser import *

def test_tokenize():
  assert_equal(tokenize('a'), ['a'])
  assert_equal(tokenize('2'), ['2'])
  assert_equal(tokenize('2.3'), ['2.3'])

  assert_equal(tokenize('ab'), list('a*b'))
  assert_equal(tokenize('a*b'), list('a*b'))
  assert_equal(tokenize('a^b'), list('a^b'))
  assert_equal(tokenize('a/b'), list('a/b'))
  assert_equal(tokenize('a * b'), list('a*b'))
  assert_equal(tokenize('a ^ b'), list('a^b'))
  assert_equal(tokenize('a / b'), list('a/b'))
  assert_equal(tokenize('a * (b)'), list('a*(b)'))
  assert_equal(tokenize('a ^ (b)'), list('a^(b)'))
  assert_equal(tokenize('a / (b)'), list('a/(b)'))
  assert_equal(tokenize('a(b)'), list('a*(b)'))

  assert_equal(tokenize('a(b)d'), list('a*(b)*d'))
  assert_equal(tokenize('a(d)e'), list('a*(d)*e'))
  assert_equal(tokenize('ade'), ['a', 'de'])
  assert_equal(tokenize('ad e'), ['a', '*', 'd', '*', 'e'])

  assert_equal(tokenize('a(b(c)(d)e)f(g)2.3(4)'), list('a*(b*(c)*(d)*e)*f*(g)*') + ['2.3'] + list('*(4)'))

  assert_equal(tokenize('a+(b)+(ab)(c)'), list('a+(b)+(a*b)*(c)'))

  assert_equal(tokenize('int x dx'), ['int', 'x', 'dx'])
  assert_equal(tokenize('int dx'), ['int', 'dx'])

  assert_equal(tokenize('int (2) + 3x * 8 dx'), ['int', '(', '2', ')', '+', '3', '*', 'x', '*', '8', 'dx'])
  assert_equal(tokenize('int (2) + 3w * 8 dz'), ['int', '(', '2', ')', '+', '3', '*', 'w', '*', '8', 'dz'])

def test_parser():
  assert_equal('NO', 'TESTS')

if __name__ == "__main__":
  do_test(test_tokenize, "tokenize")
  do_test(test_parser,   "parser")
