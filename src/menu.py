
import state
import ui

import game

class Menu(state.State):
  def __init__(self):
    super().__init__()

  def render(self) -> None:
    ui.clear()
    ui.addch(3, 3, 'MenuState')

  def input(self) -> None:
    cmd = ui.commands.getcmd()
    if cmd.is_direction():
      self.state_manager.change_state(game.Game)

  def update(self) -> None:
    pass

  def leave(self) -> None:
    pass

  def enter(self) -> None:
    pass


