
import typing

import defs
import rnd

import tilemap

__global_level_id = 0
def _next_global_level_id() -> int:
    global __global_level_id
    __global_level_id += 1
    return __global_level_id

class Level(object):

  def __init__(self, seed=None) -> None:
    super().__init__()
    self._id = _next_global_level_id()
    self._tilemap = tilemap.TileMap(defs.LEVEL_W, defs.LEVEL_H)
    self._entry = self._tilemap.random(seed)
    self._stairs_down = {sd: None for sd in self._tilemap.stairs_down} # type: Dict[Set[int, int], int]
    self._stairs_up = {su: None for su in self._tilemap.stairs_up} # type: Dict[Set[int, int], int]

  def is_blocked(self, x: int, y: int) -> bool:
    t = self._tilemap.get_tile(x, y)
    if t is None:
      return True
    if t.blocks:
      return True
    return False

  def is_visible(self, x: int, y: int) -> bool:
    t = self._tilemap.get_tile(x, y)
    if t is not None:
      if t.visible:
        return True
    return False


  entry = property(lambda s: s._entry)
  tilemap = property(lambda s: s._tilemap)
  ID = property(lambda s: s._id)
  stairs_down = property(lambda s: s._stairs_down)
  stairs_up = property(lambda s: s._stairs_up)

