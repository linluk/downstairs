
import level

class World(object):
    def __init__(self) -> None:
        super().__init__()
        lvl = level.Level()
        self._current = lvl.ID
        self._levels = {lvl.ID: lvl} # type: Dict[int, level.Level]

    current = property(lambda s: s._levels[s._current])


