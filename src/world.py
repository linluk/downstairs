
import level

MAX_DEPTH = 5

class World(object):
    def __init__(self) -> None:
        super().__init__()
        lvl = level.Level()
        self._current = lvl.ID
        self._levels = {lvl.ID: lvl} # type: Dict[int, level.Level]
        self._downstairs(lvl, MAX_DEPTH)


    def _downstairs(self, parent: level.Level, floors: int):
        if floors > 0:
            for stair_pos in parent.stairs_down.keys():
                if parent.stairs_down[stair_pos] is None:
                    lvl = level.Level()
                    self._levels[lvl.ID] = lvl
                    parent.stairs_down[stair_pos] = lvl.ID
                    self.create_downstairs(lvl, floors - 1)


    current = property(lambda s: s._levels[s._current])


