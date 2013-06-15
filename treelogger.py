class TreeLogger(object):
  """ Logger class that knows how to deal with tree-like logs """
  def __init__(self, title='root', parent=None):
    self.parent = parent
    self.title = title
    self._entries = []
    # entries e.g. [(level, logger, payload)]

  def push(self, payload):
    """ Add payload to the log """
    self._push(0, self, payload)

  def _push(self, level, log, payload):
    if not self.parent:
      self._entries.append((level, log, payload))
    else:
      self.parent._push(level + 1, log, payload)

  def split(self, title='child'):
    log = TreeLogger(title, parent=self)
    return log

  def dump(self):
    dot_titles = lambda log: '.'.join(reversed([log.title] + log.parent_titles()))  
    return '\n'.join(['{}{}) {}'.format('  '*level, dot_titles(log), payload)
      for (level, log, payload) in self._entries])

  def parent_titles(self):
    if self.parent:
      return self.parent.parent_titles() + [self.parent.title]
    else:
      return []


if __name__ == '__main__':
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
  t1.push('and back to the root')
  t1.push('we\'re done here')

  print t1.dump()

  print t1.parent_titles()
  print t2.parent_titles()
  print t2_2.parent_titles()
