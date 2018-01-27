
class State(object):
  def __init__(self):
    super().__init__()
    self._state_manager = None

  def set_state_manager(self, state_manager):
    self._state_manager = state_manager

  def render(self) -> None:
    pass

  def input(self) -> None:
    pass

  def update(self) -> None:
    pass

  def leave(self) -> None:
    pass

  def enter(self) -> None:
    pass

  state_manager = property(lambda s: s._state_manager)

StateType = type(State)

