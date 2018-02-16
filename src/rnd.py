#
# i want to have a consitent-on-all-systems
# pseudo random generator.
# this implements a Wichmann-Hill generator
#


class Random(object):
  # https://en.wikipedia.org/wiki/Wichmann%E2%80%93Hill
  __slots__ = ('_seed')

  def __init__(self, a: int = None) -> None:
    if a is None:
      import time
      a = int(time.time())
    a, x = divmod(a, 30268)
    a, y = divmod(a, 30306)
    a, z = divmod(a, 30322)
    self._seed = int(x) + 1, int(y) + 1, int(z) + 1

  def random(self) -> float:
    x, y, z = self._seed
    x = (171 * x) % 30269
    y = (172 * y) % 30307
    z = (170 * z) % 30323
    self._seed = x, y, z
    r = (x / 30269.0 + y / 30307.0 + z / 30323.0) % 1.0
    return r

  def randrange(self, low, high) -> int:
    return int(low + self.random() * (high - low))

  def randint(self, high) -> int:
    return self.randrange(0, high)

  def chance(self, probability=0.5) -> bool:
    return self.random() <= probability



_rnd = Random()

def random():
  return _rnd.random()

def randrange(low: int, high: int) -> int:
  return _rnd.randrange(low, high)

def randint(high: int) -> int:
  return _rnd.randint(high)

def chance(probability: float=0.5) -> bool:
  return _rnd.chance(probability)




if __name__ == '__main__':
  r = Random()
  for _ in range(10):
    print(r.randrange(-2,2))
  ###
  for i in range(10):
    print(r.chance(0.8))

  quit()

  ###
  d = {i: 0 for i in range(100)}
  b = False
  x = 0
  while not b:
    b = True
    for c in d.values():
      b = b and (c > 0)
      if not b:
        break
    d[r.randint(100)] += 1
    x += 1
  print('count: {}'.format(x))
  for i in range(100):
    print('{:3}: {:4}'.format(i,d[i]))

