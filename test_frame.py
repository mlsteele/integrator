import traceback

def assert_equal(a,b):
  if a != b:
    errstr = "ASSERT FAILED: %s != %s" %(a,b)
    print errstr
    raise ValueError(errstr)
  return True

def do_test(test, name):
  try:
    test()
  except Exception as ex:
    print '    ' + '\n    '.join(traceback.format_exc().split('\n'))
    print "X test FAILED: %s" %name
  else:
    print "- test passed: %s" %name
