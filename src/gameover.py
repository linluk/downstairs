
import menu
import state
import ui


class Gameover(state.State):
  def __init__(self):
    super().__init__()

  def render(self) -> None:
    ui.clear()
    ui.addch(5, 5, 'you died !!!', ui.RED, ui.BLACK, ui.BOLD)

  def input(self) -> None:
    cmd = ui.commands.getcmd()
    if cmd == ui.commands.Commands.QUIT:
      self.state_manager.terminate_main_loop()
    elif cmd == ui.commands.Commands.OK:
      self.state_manager.change_state(menu.Menu)

  def update(self) -> None:
    pass

  def leave(self) -> None:
    pass

  def enter(self) -> None:
    ui.clear()


