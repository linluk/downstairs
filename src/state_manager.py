
import state

class StateManager(object):

  def __init__(self) -> None:
    super().__init__()
    self._running = True
    self._current = None
    self._next = None
    self._states = {}

  def terminate_main_loop(self) -> None:
    self._running = False

  def add_state(self, state: state.State) -> None:
    self._states[type(state)] = state
    state.set_state_manager(self)
    if self._current is None:
      self.change_state(type(state))

  def has_state(self, state_type: state.StateType) -> bool:
    return state_type in self._states

  def change_state(self, state_type: state.StateType) -> None:
    self._next = self._states.get(state_type, None)

  def main_loop(self) -> None:
    self._running = True
    while self._running:
      if self._next is not None:
        if self._current is not None:
          self._current.leave()
        self._current = self._next
        self._current.enter()
        self._next = None
      self._current.render()
      self._current.input()
      self._current.update()


