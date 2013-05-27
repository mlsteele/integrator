from test_frame import *
from parser import *

def test_tokenize():
  assert_equal(tokenize('a'), ['a'])
  assert_equal(tokenize('2'), ['2'])
  assert_equal(tokenize('2.3'), ['2.3'])

  assert_equal(tokenize('ab'), list('a*b'))
  assert_equal(tokenize('a*b'), list('a*b'))
  assert_equal(tokenize('a * b'), list('a*b'))
  assert_equal(tokenize('a * (b)'), list('a*(b)'))
  assert_equal(tokenize('a(b)'), list('a*(b)'))

  assert_equal(tokenize('a(b)d'), list('a*(b)*d'))
  assert_equal(tokenize('a(d)e'), list('a*(e)*e'))

  assert_equal(tokenize('a(b(c)(d)e)f(g)2.3(4)'), list('a*(b*(c)*(d)*e)*f*(g)*') + ['2.3'] + list('*(4)'))

  assert_equal(tokenize('a+(b)+(ab)(c)'), list('a+(b)+(a*b)*(c)'))

  assert_equal(tokenize('int x dx'), ['int', 'x', 'dx'])

if __name__ == "__main__":
  do_test(test_tokenize,  "tokenize")
