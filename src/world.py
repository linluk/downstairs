
import level

class World(object):
  def __init__(self) -> None:
    super().__init__()
    self._levels = {} # type: Dict[int, level.Level]

  def create_levels(self):
    curr = level.Level()
    for i in range(10):
      lvl = level.Level()
      #curr.stairs_down

