class TreeLogger(object):
  def __init__(self, title='root', parent=None):
    self.title = title
    self._entries = []
    self.parent = parent
    self._children = []

  def push(self, msg):
    self._entries.append(msg)

  def split(self, title='children'):
    logger = TreeLogger(title, parent=self)
    self._children.append(logger)
    return logger

  def dump(self):
    return '\n'.join([
      '{}{}) {}'.format('  '*level, '.'.join(reversed([log.title] + log.parent_titles())), entry)
        for (level, log, entry) in self._dump_list()])

  def format(level, log, entry):
    return '\n'.join([
      '{}{}) {}'.format('  '*level, '.'.join(reversed([log.title] + log.parent_titles())), entry)
        for (level, log, entry) in self._dump_list()])

  def parent_titles(self):
    if self.parent:
      return self.parent.parent_titles() + [self.parent.title]
    else:
      return []

  def _dump_list(self):
    """ List of tuples (level, TreeLogger, entry) """
    entries = [(0, self, entry) for entry in self._entries]
    for child in self._children:
      entries += [(level + 1, log, entry) for (level, log, entry) in child._dump_list()]
    return entries


class LameLogger(object):
  def info(self, msg):
    print msg


class PrefixLogger(object):
  def __init__(self, prefix=''):
    self.prefix = prefix

  def info(self, msg):
    print self.prefix + msg

  def split(self, prefix):
    return PrefixLogger(prefix)




## example
# def tree_op(obj, log, stop=False):
#   log.info('{} foo'.format(obj))

#   if not stop:
#     tree_op('{}.a'.format(obj), log, stop=True)
#     tree_op('{}.b'.format(obj), log, stop=True)


# tree_op('obj', LameLogger())



# def tree_op(obj, log, stop=False):
#   log.info('{} foo'.format(obj))
#   if not stop:
#     tree_op('{}.a'.format(obj), log.split('  a) '), stop=True)
#     tree_op('{}.b'.format(obj), log.split('  b) '), stop=True)


# tree_op('obj', PrefixLogger())



t1 = TreeLogger()
t1.push('foo')
t2 = t1.split('split-a')
t2.push('foo_a')
t2.push('foo_a2')
t2_2 = t2.split('higher')
t2_2.push('ooh')
t2_2.push('yeah')
t3 = t1.split('split-b')
t3.push('foo_b')

print t1.dump()

print t1.parent_titles()
print t2.parent_titles()
print t2_2.parent_titles()
