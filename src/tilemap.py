
from typing import Iterator, Tuple

import rnd

import ui

class Graphic(object):  # {{{1
  __slots__ = ('ch', 'fg', 'bg', 'st')
  def __init__(self, ch: str, fg: int = ui.WHITE, bg: int = ui.BLACK, st: int = 0):
    self.ch = ch   # character. for example the @
    self.fg = fg   # foreground color
    self.bg = bg   # background color
    self.st = st   # style of font like bold

FLOOR = Graphic('.', ui.WHITE, ui.BLACK, 0)
FLOOR_SHADOW = Graphic('.', ui.GRAY, ui.BLACK, 0)

WALL = Graphic('#', ui.WHITE, ui.BLACK, 0)
WALL_SHADOW = Graphic('#', ui.GRAY, ui.BLACK, 0)

DOOR_CLOSE = Graphic('+', ui.WHITE, ui.BLACK, 0)
DOOR_CLOSE_SHADOW = Graphic('+', ui.GRAY, ui.BLACK, 0)

DOOR_OPEN = Graphic(',', ui.WHITE, ui.BLACK, 0)
DOOR_OPEN_SHADOW = Graphic(',', ui.GRAY, ui.BLACK, 0)

STAIR_DOWN = Graphic('>', ui.WHITE, ui.BLACK, 0)
STAIR_DOWN_SHADOW = Graphic('>', ui.GRAY, ui.BLACK, 0)

STAIR_UP = Graphic('<', ui.WHITE, ui.BLACK, 0)
STAIR_UP_SHADOW = Graphic('<', ui.GRAY, ui.BLACK, 0)

class Tile(object):  # {{{1
  __slots__ = ('_blocks', '_opaque', '_graphic_shadow', '_graphic', '_explored', '_visible') # type: ignore
  def __init__(self, blocks: bool, opaque: bool, graphic: Graphic, graphic_shadow: Graphic) -> None:
    super().__init__()
    self._blocks = blocks
    self._opaque = opaque
    self._graphic = graphic
    self._graphic_shadow = graphic_shadow
    self._explored = False
    self._visible = False

  def set_visible(self, visible):
    self._visible = visible
    self._explored = self._explored or visible

  def get_graphic(self):
    return self._graphic if self._visible else self._graphic_shadow

  def draw(self, x: int, y: int):
    g = self.get_graphic()
    ui.addch(x, y, g.ch, g.fg, g.bg, g.st)

  blocks = property(lambda s: s._blocks)
  opaque = property(lambda s: s._opaque)
  explored = property(lambda s: s._explored)
  visible = property(lambda s: s._visible, set_visible)


class FloorTile(Tile):
  def __init__(self):
    super().__init__(False, False, FLOOR, FLOOR_SHADOW)


class WallTile(Tile):
  def __init__(self):
    super().__init__(True, True, WALL, WALL_SHADOW)

class StairsDownTile(Tile):
  def __init__(self):
    super().__init__(False, False, STAIR_DOWN, STAIR_DOWN_SHADOW)

class StairsUpTile(Tile):
  def __init__(self):
    super().__init__(False, False, STAIR_UP, STAIR_UP_SHADOW)

class Door(Tile):
  __slots__ = ('_closed') # type: ignore
  def __init__(self):
    super().__init__(True, True, None, None)
    self._graphic = [DOOR_OPEN, DOOR_CLOSE]
    self._graphic_shadow = [DOOR_OPEN_SHADOW, DOOR_CLOSE_SHADOW]
    self._closed = False
    self.toggle() # toggle it to close

  def toggle(self):
    self._closed = not self._closed
    self._blocks = self._closed
    self._opaque = self._closed

  def get_graphic(self):
    i = 1 if self._closed else 0
    return super().get_graphic()[i]

# }}}


class TileMap(object):  # {{{1
  __slots__ = ('_width', '_height', '_tiles', '_stairs_down', '_stairs_up')
  def __init__(self, width: int = 79, height: int = 35) -> None:
    super().__init__()
    self._width = width
    self._height = height
    self._stairs_down = []
    self._stairs_up = []
    self._tiles = [[None for y in range(height)] for x in range(width)]


  def get_tile(self, x: int, y: int) -> Tile:
    return self._tiles[x][y]

  def get_tiles(self) -> Iterator[Tuple[Tuple[int, int], Tile]]:
    for x in range(self._width):
      for y in range(self._height):
        t = self._tiles[x][y]
        if t:
          yield ((x, y), t)

  tiles = property(lambda s: s._tiles)
  width = property(lambda s: s._width)
  height = property(lambda s: s._height)

  def fov(self, x, y, r): #{{{2
    # reset visibility
    for cx in range(self._width):
      for cy in range(self._height):
        if self._tiles[cx][cy] is not None:
          self._tiles[cx][cy].visible = False
    # calculate visible _tiles
    for cx in range(max(x-r, 0), min(x+r+1, self._width)):
      for cy in range(max(y-r, 0), min(y+r+1, self._height)):
        if self._tiles[cx][cy] is not None:
          if r >= ((max(x, cx) - min(x, cx)) ** 2 + (max(cy, y) - min(cy, y)) ** 2) ** 0.5:
            v = self.los(x, y, cx, cy)
            self._tiles[cx][cy].visible = v
          else:
            self._tiles[cx][cy].visible = False

  def los(self, x1, y1, x2, y2): #{{{2
    """ returns True if you can see from (x1, y1) to (x2, y2) """
    if x1 == x2 and y1 == y2:
      return True
    dx = x1 - x2
    dy = y1 - y2
    adx = abs(dx)
    ady = abs(dy)
    sign_x = -1 if dx < 0 else 1
    sign_y = -1 if dy < 0 else 1
    x = x2
    y = y2
    # different versions for x or y dominated lines
    if adx > ady:
      # x dominated
      t = ady * 2 - adx
      while True:
        if t >= 0:
          y += sign_y
          t -= (adx * 2)
        x += sign_x
        t += (ady * 2)
        if x == x1 and y == y1:
          return True
        if self._tiles[x][y] is not None:
          if self._tiles[x][y].opaque:
            return False
    else:
      # y dominated
      t = adx * 2 - ady
      while True:
        if t >= 0:
          x += sign_x
          t -= (ady * 2)
        y += sign_y
        t += (adx * 2)
        if x == x1 and y == y1:
          return True
        if self._tiles[x][y] is not None:
          if self._tiles[x][y].opaque:
            return False


  def random(self, seed=None): #{{{2
    rand = rnd.Random(seed)
    failcount = 0
    last = None
    while failcount <= 25:
      # generate a room
      _width, _height = rand.randrange(2, self._width // 3), rand.randrange(2, self._height // 3)
      top, left = rand.randrange(1, self._height - _height - 2), rand.randrange(1, self._width - _width - 2)
      # check if it overlaps with another room
      overlaps = False
      for x in range(left, left + _width + 1):
        for y in range(top, top + _height + 1):
          if not self._tiles[x][y] is None:
            overlaps = True
            break
        if overlaps:
          break
      # if it overlaps try to generate another one
      if overlaps:
        failcount += 1
        continue
      failcount = 0
      # if it does not overlap "draw" it
      for x in range(left, left + _width + 1):
        for y in range(top, top + _height + 1):
          self._tiles[x][y] = FloorTile()
      # if it was not the first room
      if last is not None:
        # connect with last room
        act = (left + rand.randrange(1, _width), top + rand.randrange(1, _height))
        low = min(last[0], act[0])
        high = max(last[0], act[0])
        door = rand.chance(0.5)
        for x in range(low, high + 1):
          if self._tiles[x][last[1]] is None:
            if door:
              self._tiles[x][last[1]] = Door()
              if rand.chance(0.1):
                self._tiles[x][last[1]].toggle()
              door = False
            else:
              self._tiles[x][last[1]] = FloorTile()
        low = min(last[1], act[1])
        high = max(last[1], act[1])
        door = rand.chance(0.5)
        for y in range(low, high + 1):
          if self._tiles[act[0]][y] is None:
            if door:
              self._tiles[act[0]][y] = Door()
              if rand.chance(0.1):
                self._tiles[act[0]][y].toggle()
              door = False
            else:
              self._tiles[act[0]][y] = FloorTile()
      else:
        #we are in the "first room"
        # so we should have stairs down
        stair_x, stair_y = left + rand.randrange(1, _width), top + rand.randrange(1, _height)
        self._tiles[stair_x][stair_y] = StairsDownTile()
        self._stairs_down.append((stair_x, stair_y))
      # save the act. center as last
      last = (left + rand.randrange(1, _width), top + rand.randrange(1, _height))

    # we generated all rooms
    # so we add stairs up
    stair_x, stair_y = left + rand.randrange(1, _width), top + rand.randrange(1, _height)
    self._tiles[stair_x][stair_y] = StairsUpTile()
    self._stairs_up.append((stair_x, stair_y))

    # draw walls around floors
    for x in range(self._width):
      for y in range(self._height):
        # ofcourse only on empty _tiles
        if self._tiles[x][y] is not None:
          continue
        # get all potential neighbours
        n = [(x-1,y-1),(x,y-1),(x+1,y-1),
            (x-1,y),          (x+1,y),
            (x-1,y+1),(x,y+1),(x+1,y+1)]
        for c in n:
          # if the neighbor is valid
          if (0 <= c[0] < self._width) and (0 <= c[1] < self._height):
            # and is None
            #if isinstance(self._tiles[c[0]][c[1]], FloorTile):
            if (self._tiles[c[0]][c[1]] is not None) and (not isinstance(self._tiles[c[0]][c[1]], WallTile)):
              # draw a wall
              self._tiles[x][y] = WallTile()
              break

    # return center of last room (maybe the player wants to start here).
    return last


