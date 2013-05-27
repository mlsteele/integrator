from elements import *

# TODO condense these constants
BIN_OPS = ['*', '+', '/', '-']
PARENS = [['(', ')'], ['[', ']']]
PARENS_FLAT = ['(', ')', '[', ']']
LEFT_PARENS  = ['(', '[']
RIGHT_PARENS = [')', ']']
OPERATORS = ["*", "+", "/", "-","(",")","[","]"]

class ParseError(Exception): pass

def tokenize(s):
  def isnum(s): return s.isdigit() or s == '.'

  character_stream = list(s)
  tokens = []

  tokens.append(character_stream[0])
  character_stream = character_stream[1:]

  while len(character_stream) > 0:
    char = character_stream[0]
    character_stream = character_stream[1:]

    # process char into tokens
    # catch spaces
    if char == ' ':
      pass
    elif isnum(tokens[-1]):
      # number -> number
      if isnum(char):
        tokens[-1] += char
      # number -> symbol
      if char in VariableSet.SYMBOLS:
        tokens += ['*', char]
      else:
        tokens.append(char)
    elif tokens[-1] in VariableSet.SYMBOLS:
      # symbol -> symbol
      if char in VariableSet.SYMBOLS:
        tokens += ['*', char]
      else:
        tokens.append(char)
    elif tokens[-1] in PARENS_FLAT:
      # paren -> paren
      if char in PARENS_FLAT:
        tokens += ['*', char]
      else:
        tokens.append(char)
    else:
      tokens.append(char)

  # remove spaces
  tokens = filter(lambda t: t != ' ', tokens)

  return tokens

def parse_tokens(tokens, vset=None, debug=False):
  zip3 = lambda l: zip(l, l[1:], l[2:])

  # scan left to right and apply binary expressions
  def scan_binops(tokens, binops):
    # while there are operators in tokens
    while len(set(binops.keys()).intersection(set(tokens[1:-1]))) > 0:
      first_index = (i for i,v in enumerate(tokens) if v in binops.keys()).next()
      l,t,r = tokens[first_index - 1], tokens[first_index], tokens[first_index + 1]

      if isinstance(l, str) or isinstance(r, str):
        raise ParseError("left or right of binop is a string\n    l: %s\n    r: %s" %(l,r))

      new_token = binops[t](l,t,r)
      tokens = tokens[0:first_index - 1] + [new_token] + tokens[first_index + 2:]
    return tokens

  # scan left to right and grouping operators (like parens)
  def scan_groups(tokens, split_l, split_r):
    # while there are both left and right splitters in tokens
    # while len(set([split_l, split_r]).intersection(set(tokens))) == 2:
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


      new_token = parse_tokens(inner_tokens, debug=debug)
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
    if isinstance(token, str) and token.isdigit():
      return Number(float(token))
    else:
      return token
  tokens = [numbers(t) for t in tokens]

  # parens
  if debug: print "    parsing parens"
  tokens = scan_groups(tokens, '(', ')')

  # multiplication
  # TODO division
  if debug: print "    parsing multiplication"
  binops = {
    '*': lambda l,t,r: Product(l, r) }
    # '-': lambda l,t,r: Sum(l, Product(Number(-1), r)) }
  tokens = scan_binops(tokens, binops)

  # addition, subtraction
  if debug: print "    parsing addition, subtraction"
  binops = {
    '+': lambda l,t,r: Sum(l, r) ,
    '-': lambda l,t,r: Sum(l, Product(Number(-1), r)) }
  tokens = scan_binops(tokens, binops)

  # TODO integration

  # check for unparsed tokens
  for t in tokens:
    if isinstance(t, str):
      raise ParseError("unparsed token '%s'" %t)

  if len(tokens) != 1:
    raise ParseError("resultant tokens length is not 1 (%s)" %len(tokens))

  return tokens[0]


# s = "(3x + 53)*24"
# s = "((2 + 3) * 5h) * (3 + f)"
s = "(3)(2a)"
print s
ts = tokenize(s)
print "tokens: %s" % ts
p = parse_tokens(ts, debug=False)
print p
print p.simplified()

a = [1,2,'+',3,'+',4,5,6,7,'*',8,10]
# print a
