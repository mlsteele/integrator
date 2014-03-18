"""
Parser for integral expressions.

The parse function of this module parses a string
into an expressions made of elements from elements.py

The implementation is verbose and hard to read.
It will be replaced soon, and the addition of new features
to parse will be more possible.
Until that day, tests/test_parser can help make sure
that this module behaves itself.
"""

import re
from elements import *

# TODO remove redundancy from these constants
BIN_OPS = ['*', '+', '/', '-', '^']
INTG_START = 'int'
PARENS = [['(', ')'], ['[', ']']]
PARENS_FLAT = ['(', ')', '[', ']']
PARENS_LEFT  = ['(', '[']
PARENS_RIGHT = [')', ']']
OPERATORS = ["*", "+", "/", "-","(",")","[","]"]


class ParseError(Exception): pass


def _isnum(s):
  return bool(re.match('\d*\.?\d*$', s))


def tokenize(s):
  character_stream = list(s)
  tokens = [' '] # initial space eases logic edge cases

  # process chars into tokens
  while len(character_stream) > 0:
    char = character_stream[0]

    # recue integrals starts
    #WARN: this section advances on its own and then continues to a
    # new state of the loop
    if character_stream[0:len(INTG_START)] == list(INTG_START):
      tokens.append(INTG_START)
      # advance character stream an EXTRA 2 notches
      character_stream = character_stream[len(INTG_START):]
      continue
    # catch integral stops
    if character_stream[0] == 'd' and len(character_stream) >= 2 and character_stream[1] in VariableSet.SYMBOLS:
      tokens.append('d' + character_stream[1])
      character_stream = character_stream[2:]
      continue


    def default(char):
      if _isnum(char) or char in VariableSet.SYMBOLS.union(set(BIN_OPS), set(PARENS_FLAT)):
        tokens.append(char)
      else:
        raise ParseError("uknown char to tokenize: %s" %char)

    # catch spaces
    if char == ' ':
      pass
    elif _isnum(tokens[-1]):
      # number -> number
      if _isnum(char):
        tokens[-1] += char
      # number -> (symbol | left paren)
      elif char in VariableSet.SYMBOLS or char in PARENS_LEFT:
        tokens += ['*', char]
      else:
        default(char)
    elif tokens[-1] in VariableSet.SYMBOLS:
      # symbol -> (symbol | number | left paren)
      if char in VariableSet.SYMBOLS or _isnum(char) or char in PARENS_LEFT:
        tokens += ['*', char]
      else:
        default(char)
    elif tokens[-1] in PARENS_RIGHT:
      if char in PARENS_LEFT or char in VariableSet.SYMBOLS or _isnum(char):
        tokens += ['*', char]
      else:
        default(char)
    elif tokens[-1] in PARENS_LEFT:
      # paren -> paren
      if char in PARENS_FLAT:
        tokens += [char]
      else:
        default(char)
    else:
      default(char)

    # advance character stream
    character_stream = character_stream[1:]

  return tokens[1:] # remove initial space


def parse_tokens(tokens, vset=None, debug=False):
  zip3 = lambda l: zip(l, l[1:], l[2:])

  # scan left to right and apply binary expressions
  def scan_binops(tokens, binops):
    # while there are operators in tokens
    while len(set(binops.keys()).intersection(set(tokens[1:-1]))) > 0:
      first_index = (i for i,v in enumerate(tokens) if v in binops.keys()).next()
      l,t,r = tokens[first_index - 1], tokens[first_index], tokens[first_index + 1]

      if isinstance(l, str) or isinstance(r, str):
        raise ParseError("left or right of binop is a string\n    l: {0!r}\n    r: {1!r}".format(l,r))

      new_token = binops[t](l,t,r)
      tokens = tokens[0:first_index - 1] + [new_token] + tokens[first_index + 2:]
    return tokens

  # scan left to right and grouping operators e.g. parens
  def scan_groups(tokens, vset, split_l, split_r):
    # while there are both left and right splitters in tokens
    while split_l in tokens and split_r in tokens:
      split_left_index = (i for i,v in enumerate(tokens) if v in [split_l]).next()

      # find matching splitter
      depth_counter = 1
      split_right_index = split_left_index
      for t in tokens[split_left_index + 1:]:
        split_right_index += 1

        if t == split_l:
          depth_counter += 1
        if t == split_r:
          depth_counter -= 1
          if depth_counter == 0:
            break

      if split_right_index > len(tokens):
        raise ParseError('unmatched left splitter for "%s %s"' %(split_l, split_r))

      # break tokens into parts
      left_tokens  = tokens[: split_left_index]
      inner_tokens = tokens[split_left_index + 1 : split_right_index]
      right_tokens = tokens[split_right_index + 1 :]
      if debug: print "left_tokens : %s" % str(left_tokens)
      if debug: print "inner_tokens: %s" % str(inner_tokens)
      if debug: print "right_tokens: %s" % str(right_tokens)

      new_token = parse_tokens(inner_tokens, vset=vset, debug=debug)
      if debug: print "new_token: %s" % str(new_token)
      tokens = left_tokens + [new_token] + right_tokens

    return tokens

  # modified scan_groups for integrals (no nested counting, 'dx' variable capture)
  def scan_integrals(tokens, vset):
    while INTG_START in tokens:
      split_left_index = (i for i,v in enumerate(tokens) if v == INTG_START).next()

      # find matching splitter
      is_right_split = lambda t: isinstance(t,str) and t[0] == 'd' and t[1:] in VariableSet.SYMBOLS
      split_right_index = split_left_index + (i for i,v in enumerate(tokens[split_left_index:]) if is_right_split(v)).next()

      if split_right_index > len(tokens):
        raise ParseError('unmatched integral start')

      # break tokens into parts
      left_tokens  = tokens[: split_left_index]
      inner_tokens = tokens[split_left_index + 1 : split_right_index]
      right_tokens = tokens[split_right_index + 1 :]
      if debug: print "left_tokens : %s" % str(left_tokens)
      if debug: print "inner_tokens: %s" % str(inner_tokens)
      if debug: print "right_tokens: %s" % str(right_tokens)

      new_inner_token = parse_tokens(inner_tokens, vset=vset, debug=debug)
      intg_var = vset.variable(tokens[split_right_index][1:])
      new_token = Integral(new_inner_token, intg_var)
      if debug: print "new_token: %s" % str(new_token)
      tokens = left_tokens + [new_token] + right_tokens

    return tokens

  # # # #

  if debug: print "parsing tokens: %s" % str(tokens)

  if vset == None:
    vset = VariableSet()
  if not isinstance(vset, VariableSet):
    raise ValueError('vset is not instance of VariableSet')

  # variables
  if debug: print "    parsing variables"
  def variables(token):
    if token in vset.SYMBOLS:
      return vset.variable(token)
    else:
      return token
  tokens = [variables(t) for t in tokens]

  # numbers
  if debug: print "    parsing numbers"
  def numbers(token):
    # TODO floats?
    if isinstance(token, str) and _isnum(token):
      return Number(int(token))
    else:
      return token
  tokens = [numbers(t) for t in tokens]

  # parens
  if debug: print "    parsing parens"
  tokens = scan_groups(tokens, vset, '(', ')')

  # power
  if debug: print "    parsing powers"
  binops = {
    '^': lambda l,t,r: Power(l, r) }
  tokens = scan_binops(tokens, binops)

  # multiplication
  # TODO division
  if debug: print "    parsing multiplication"
  binops = {
    '*': lambda l,t,r: Product(l, r) ,
    '/': lambda l,t,r: Fraction(l, r) }
  tokens = scan_binops(tokens, binops)

  # addition, subtraction
  if debug: print "    parsing addition, subtraction"
  binops = {
    '+': lambda l,t,r: Sum(l, r) ,
    '-': lambda l,t,r: Sum(l, Product(Number(-1), r)) }
  tokens = scan_binops(tokens, binops)

  # TODO integration
  tokens = scan_integrals(tokens, vset)

  # check for unparsed tokens
  for t in tokens:
    if isinstance(t, str):
      raise ParseError("unparsed token '%s'" %t)

  if len(tokens) != 1:
    raise ParseError("resultant tokens length is not 1 (%s)" %len(tokens))

  return tokens[0]


def parse(s, vset=None, debug=False):
  return parse_tokens(tokenize(s), vset=vset, debug=debug)

if __name__ == "__main__":
  s = 'int 2*2x^(3) dx'
  print "string: \"%s\"" %s
  ts = tokenize(s)
  print "tokens: %s" %ts
  p = parse_tokens(ts)
  print "parsed: %s" %p
  print "simplified: %s" %p.simplified()
