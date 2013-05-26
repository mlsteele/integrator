from elements import *

BIN_OPS = ['*', '+', '/', '-']
PARENS = [['(', ')'], ['[', ']']]
OPERATORS = ["*", "+", "/", "-","(",")","[","]"]

class ParseError(Exception): pass

def tokenize(s):
  noSpaces = s.replace(" ","")

  lastInd = 0 # last measured index of a key
  splitStrings = []

  for ind in range(len(noSpaces)):
    if noSpaces[ind] in OPERATORS:
      splitStrings += [noSpaces[lastInd:ind], noSpaces[ind:ind+1]]
      lastInd = ind + 1

  splitStrings += [noSpaces[lastInd:]]
  splitStrings = [e for e in splitStrings if e != ""]

  return splitStrings

def parse_tokens(tokens):
  zip3 = lambda l: zip(l, l[1:], l[2:])

  def scan_binops(binops, tokens):
    while len(set(binops.keys()).intersection(set(tokens))) > 0:
      first_index = (i for i,v in enumerate(tokens) if v in binops.keys()).next()
      l,t,r = tokens[first_index - 1], tokens[first_index], tokens[first_index + 1]

      if isinstance(l, str) or isinstance(r, str):
        raise ParseError("parse error: left or right of binop is a string\n    l: %s\n    r: %s" %(l,r))

      new_token = binops[t](l,t,r)
      tokens = tokens[0:first_index - 1] + [new_token] + tokens[first_index + 2:]
    return tokens

  # # # #

  vset = VariableSet()

  # variables
  def variables(token):
    if token in vset.SYMBOLS:
      return vset.variable(token)
    else:
      return token
  tokens = [variables(t) for t in tokens]

  # numbers
  def numbers(token):
    # TODO floats?
    if token.isdigit():
      return Number(float(token))
    else:
      return token
  tokens = [numbers(t) for t in tokens]

  # TODO parens


  # multiplication
  # TODO division
  binops = {
    '*': lambda l,t,r: Product(l, r) }
    # '-': lambda l,t,r: Sum(l, Product(Number(-1), r)) }
  tokens = scan_binops(binops, tokens)

  # addition
  binops = {
    '+': lambda l,t,r: Sum(l, r) ,
    '-': lambda l,t,r: Sum(l, Product(Number(-1), r)) }
  tokens = scan_binops(binops, tokens)

  # TODO integration

  # check for unparsed tokens
  for t in tokens:
    if isinstance(t, str):
      raise ParseError("parse error: unparsed token '%s'" %t)

  if len(tokens) != 1:
    raise ParseError("parse error: resultant tokens length is not 1 (%s)" %len(tokens))

  return tokens[0]


# s = "(3x + 53)*24"
s = "2 + 3 * 5"
print s
print parse_tokens(tokenize(s))
print parse_tokens(tokenize(s)).simplified()

a = [1,2,'+',3,'+',4,5,6,7,'*',8,10]
# print a
