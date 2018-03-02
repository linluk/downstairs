
import typing

import defs
import rnd

import tilemap

class Level(object):

  def __init__(self) -> None:
    super().__init__()
    self._tilemap = tilemap.TileMap(defs.LEVEL_W, defs.LEVEL_H)
    self._entry = self._tilemap.random()

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

