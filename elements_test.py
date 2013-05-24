from elements import *

def assert_equal(a,b):
  if a != b:
    errstr = "ASSERT FAILED: %s != %s" %(a,b)
    raise Exception(errstr)
  return True

if __name__ == "__main__":
  print assert_equal(0,1)
