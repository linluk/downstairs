
from typing import Tuple

import utils

import ui
import ecs

class MoveOrAttack(ecs.Component):
  def __init__(self):
    super().__init__()
    self._dx = 0
    self._dy = 0

  def _set(self, dxdy: Tuple[int, int]) -> None:
    self._dx, self._dy = dxdy

  def _get(self) -> Tuple[int, int]:
    return (self._dx, self._dy)

  dxdy = property(_get, _set)
  dx = property(lambda s: s._dx, lambda s, x: s._set((x, s._dy)))
  dy = property(lambda s: s._dy, lambda s, y: s._set((s._dx, y)))

class Name(ecs.Component):
  def __init__(self, name: str):
    super().__init__()
    self._name = name

  name = property(lambda s: s._name)


class Player(ecs.Component):
  def __init__(self):
    super().__init__()


class Door(ecs.Component):
  ### TODO: the commented key could be useful :-)
  def __init__(self):
    super().__init__()
    self._x = 0
    self._y = 0
#    self._key = None

  def _set_xy(self, xy) -> None:
    self._x, self._y = xy

  def _get_xy(self) -> Tuple[int, int]:
    return (self._x, self._y)

#  def _set_key(self, key):
#    self._key = key

  xy = property(_get_xy, _set_xy)
  x = property(lambda s: s._x, lambda s, x: s._set_xy((x, s._y)))
  y = property(lambda s: s._y, lambda s, y: s._set_xy((s._x, y)))

#  key = property(lambda s: s._key, _set_key)



class Position(ecs.Component):
  __slots__ = ('_x', '_y')
  def __init__(self, x: int = 0, y: int = 0):
    super().__init__()
    self._x = x
    self._y = y

  def _set(self, xy) -> None:
    self._x, self._y = xy

  def _get(self) -> Tuple[int, int]:
    return (self._x, self._y)

  xy = property(_get, _set)
  x = property(lambda s: s._x, lambda s, x: s._set((x, s._y)))
  y = property(lambda s: s._y, lambda s, y: s._set((s._x, y)))


class Blocking(ecs.Component):
  __slots__ = ('_value', )
  def __init__(self, value: bool = True):
    super().__init__()
    self._value = value

  def _set(self, value: bool) -> None:
    self._value = value

  value = property(lambda s: s._value, _set)


class Sight(ecs.Component):
  __slots__ = ('_radius', )
  def __init__(self, radius: float):
    super().__init__()
    self._radius = radius

  radius = property(lambda s: s._radius)


class Graphics(ecs.Component):
  __slots__ = ('ch', 'fg', 'bg', 'st')
  def __init__(self, ch: str, fg: int = ui.WHITE, bg: int = ui.BLACK, st: int = 0):
    super().__init__()
    self.ch = ch   # character. for example the @
    self.fg = fg   # foreground color
    self.bg = bg   # background color
    self.st = st   # style of font like bold


class CombatStats(ecs.Component):

  def __init__(self):
    super().__init__()
    self._acc = 0 # type: float  # accuracy
    self._atk = 0 # type: float  # attack
    self._def = 0 # type: float  # defense
    self._hpm = 1 # type: int    # health max
    self._hp = self._hpm # type: int  # health

  def _set_acc(self, value: int) -> None:
    self._acc = value
  def _set_atk(self, value: int) -> None:
    self._atk = value
  def _set_def(self, value: int) -> None:
    self._def = value
  def _set_hpm(self, value: int) -> None:
    self._hpm = value
  def _set_hp(self, value: int) -> None:
    self._hp = value

  ACC = property(lambda s: s._acc, _set_acc)
  ATK = property(lambda s: s._acc, _set_acc)
  DEF = property(lambda s: s._def, _set_def)
  HPM = property(lambda s: s._hpm, _set_hpm)
  HP = property(lambda s: s._hp, _set_hp)


all_components = [cls for cls in utils.classes_from_module(__name__, lambda c: issubclass(c, ecs.Component))]

##############################################################################
##############################################################################
##############################################################################


#"""
#class Ai(ecs.Component):
#  def __init__(self, entity: object):
#    super().__init__(entity)
#
#  def update(self):
#    if self.entity.level.player is None: return None
#    px, py = self.entity.level.player.position.get_xy()
#    if self.entity.sight is None: return None
#    if not self.entity.sight.can_see(px, py): return None
#    x, y = self.entity.position.get_xy()
#    dx = max(px, x) - min(px, x)
#    dy = max(py, y) - min(py, y)
#    if (dx + dy) == 1:
#      self.entity.combat.attack_xy(px, py)
#      return None
#    if dx < dy: self.entity.moving.move(0, 1 if py > y else -1)
#    elif dx > dy: self.entity.moving.move(1 if px > x else -1, 0)
#    else:
#      rand = rnd.Random()
#      if rand.chance():
#        self.entity.moving.move(0, 1 if py > y else -1)
#      else:
#        self.entity.moving.move(1 if px > x else -1, 0)
#"""



