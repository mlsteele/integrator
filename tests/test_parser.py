import unittest

from parser import *

class TestElements(unittest.TestCase):
  def test_tokenize(self):
    self.assertEqual(tokenize('a'), ['a'])
    self.assertEqual(tokenize('2'), ['2'])
    self.assertEqual(tokenize('2.3'), ['2.3'])

    self.assertEqual(tokenize('ab'), list('a*b'))
    self.assertEqual(tokenize('a*b'), list('a*b'))
    self.assertEqual(tokenize('a^b'), list('a^b'))
    self.assertEqual(tokenize('a/b'), list('a/b'))
    self.assertEqual(tokenize('a * b'), list('a*b'))
    self.assertEqual(tokenize('a ^ b'), list('a^b'))
    self.assertEqual(tokenize('a / b'), list('a/b'))
    self.assertEqual(tokenize('a * (b)'), list('a*(b)'))
    self.assertEqual(tokenize('a ^ (b)'), list('a^(b)'))
    self.assertEqual(tokenize('a / (b)'), list('a/(b)'))
    self.assertEqual(tokenize('a(b)'), list('a*(b)'))

    self.assertEqual(tokenize('a(b)d'), list('a*(b)*d'))
    self.assertEqual(tokenize('a(d)e'), list('a*(d)*e'))
    self.assertEqual(tokenize('ade'), ['a', 'de'])
    self.assertEqual(tokenize('ad e'), ['a', '*', 'd', '*', 'e'])

    self.assertEqual(tokenize('a(b(c)(d)e)f(g)2.3(4)'), list('a*(b*(c)*(d)*e)*f*(g)*') + ['2.3'] + list('*(4)'))

    self.assertEqual(tokenize('a+(b)+(ab)(c)'), list('a+(b)+(a*b)*(c)'))

    self.assertEqual(tokenize('int x dx'), ['int', 'x', 'dx'])
    self.assertEqual(tokenize('int dx'), ['int', 'dx'])

    self.assertEqual(tokenize('int (2) + 3x * 8 dx'), ['int', '(', '2', ')', '+', '3', '*', 'x', '*', '8', 'dx'])
    self.assertEqual(tokenize('int (2) + 3w * 8 dz'), ['int', '(', '2', ')', '+', '3', '*', 'w', '*', '8', 'dz'])

  def test_parser(self):
    self.assertEqual('NO', 'TESTS')


if __name__ == '__main__':
  unittest.main()
