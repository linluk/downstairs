
import state
import ui

import game
import defs

from collections import namedtuple

MenuItem = namedtuple('MenuItem', ['name', 'state'])

class Menu(state.State):
  def __init__(self):
    super().__init__()
    self._idx = 0
    self._width = 0
    self._menu_items = [] #

  def add_item(self, name, state):
    item = MenuItem(name, state)
    self._menu_items.append(item)
    if len(name) > self._width:
      self._width = len(name)

  def render(self) -> None:
    ui.clear()
    x = (defs.SCREEN_W // 2) - ((self._width + 3) // 2)
    y = (defs.SCREEN_H // 2) - (len(self._menu_items) // 2)
    for i in range(len(self._menu_items)):
      item = self._menu_items[i]
      ui.addch(x, y + i, '[{}] {}'.format('X' if i == self._idx else ' ', item.name))

  def input(self) -> None:
    cmd = ui.commands.getcmd()
    if cmd == ui.commands.Commands.NORTH:
      self._idx -= 1
      if self._idx < 0:
        self._idx = len(self._menu_items) - 1
    if cmd == ui.commands.Commands.SOUTH:
      self._idx += 1
      if self._idx >= len(self._menu_items):
        self._idx = 0
    if cmd == ui.commands.Commands.OK:
      state = self._menu_items[self._idx].state
      if state is None:
        self.state_manager.terminate_main_loop()
      else:
        self.state_manager.change_state(state)

  def update(self) -> None:
    pass

  def leave(self) -> None:
    pass

  def enter(self) -> None:
    ui.clear()


