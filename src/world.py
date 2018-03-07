
import level
import rnd

MAX_DEPTH = 5

class World(object):
    def __init__(self) -> None:
        super().__init__()
        self._random = rnd.Random()
        lvl = level.Level(self._random.randint(65535))
        self._current = lvl.ID
        self._levels = {lvl.ID: lvl} # type: Dict[int, level.Level]
        self._downstairs(lvl, MAX_DEPTH)


    def _downstairs(self, parent: level.Level, floors: int):
        if floors > 0:
            for stair_pos in parent.stairs_down.keys():
                if parent.stairs_down[stair_pos] is None:
                    lvl = level.Level(self._random.randint(65535))
                    self._levels[lvl.ID] = lvl
                    parent.stairs_down[stair_pos] = lvl.ID
                    tmp = next(iter(lvl.stairs_up.keys()))
                    if tmp is not None:
                        lvl.stairs_up[tmp] = parent.ID
                    self._downstairs(lvl, floors - 1)


    current = property(lambda s: s._levels[s._current])


