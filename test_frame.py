import traceback

class AssertionError(Exception):
  def __init__(self, a, b):
    self.a = a
    self.b = b

def assert_equal(a,b):
  if a != b:
    # errstr = "ASSERT FAILED: %s != %s" %(a,b)
    raise AssertionError(a, b)
  return True

def assert_true(x):
  return assert_equal(x, True)

def assert_false(x):
  return assert_equal(x, False)

def assert_bool(true=None, false=None):
  true_pass  = assert_true(true)   if true  != None else True
  false_pass = assert_false(false) if false != None else True
  return true_pass and false_pass

def assert_fail():
  raise AssertionError('Assertion', 'Failed')

def do_test(test, name):
  try:
    test()
  except AssertionError as ex:
    print "ASSERTION FAILED: %s != %s" %(str(ex.a), str(ex.b))
    print '    ' + '\n    '.join(traceback.format_exc().split('\n'))[:-5]
    print 2*'    ' + str(ex.a)
    print 2*'    ' + str(ex.b)
    print ''
    print "X test FAILED: %s" %name
  except Exception as ex:
    print '    ' + '\n    '.join(traceback.format_exc().split('\n'))
    print ''
    print "X test FAILED: %s" %name
  else:
    print "- test passed: %s" %name
