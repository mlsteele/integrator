from elements import *
from strategies import *
from parser import parse

if __name__ == "__main__":
  s = raw_input("enter expression string: ")
  expr = parse(s)
  print expr
