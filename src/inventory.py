
import state
import ui
import components

import game
import defs

from collections import namedtuple

InventoryItem = namedtuple('InventoryItem', ['name', 'entity'])

class Inventory(state.State):
  def __init__(self):
    super().__init__()
    self._idx = 0
    self._width = 0
    self._items = None # type:component.Items

  def set_items(self, items):
    self._items = items

  def render(self) -> None:
    ui.clear()
    x = (defs.SCREEN_W // 2) - ((self._width + 3) // 2)
    y = 10
    for i in range(len(self._items.items)):
      item = self._items.items[i]
      ui.addch(x, y + i, '[{}] {}'.format('X' if i == self._idx else ' ', item.get_component(components.Name).name))

  def input(self) -> None:
    cmd = ui.commands.getcmd()
    if cmd == ui.commands.Commands.NORTH:
      self._idx -= 1
      if self._idx < 0:
        self._idx = len(self._items.items) - 1
    if cmd == ui.commands.Commands.SOUTH:
      self._idx += 1
      if self._idx >= len(self._items.items):
        self._idx = 0
    if cmd == ui.commands.Commands.OK:
      self.state_manager.change_state(game.Game)

  def update(self) -> None:
    pass

  def leave(self) -> None:
    pass

  def enter(self) -> None:
    ui.clear()


