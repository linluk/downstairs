
import ui
import ui.commands
from ui.commands import Commands
import tilemap
import defs



import level

import sys

import time
import rnd

import monsters
import items
import systems
import components
import ecs

import state
import menu

class Game(state.State):

  def __init__(self):
    super().__init__()
    self.level = level.Level()

    self._entity_list = []

    self._user_input = systems.UserInput()
    self._user_input.on_quit = self.quit

    self._turn = systems.Turn()
    self._turn.check_blocked = self.level.is_blocked
    self._turn.on_moved = self.moved
    self._turn.toggle_door = self.toggle_door

    self._rendering = systems.Rendering(defs.LEVEL_X, defs.LEVEL_Y)
    self._rendering.check_visible = self.level.is_visible

  def calc_fov_if_player(self, entity: ecs.Entity):
    if entity.has_component(components.Player):
      sight = entity.get_component(components.Sight) # type: components.Sight
      self.level.tilemap.fov(*entity.get_component(components.Position).xy, sight.radius)


  def quit(self):
    #self.state_manager.terminate_main_loop()
    self.state_manager.change_state(menu.Menu)

  def moved(self, entity: ecs.Entity):
    self.calc_fov_if_player(entity)

  def toggle_door(self, entity, x, y):
    t = self.level.tilemap.get_tile(x, y)
    if isinstance(t, tilemap.Door):
      t.toggle()
      self.calc_fov_if_player(entity)
      return True
    return False

  def render(self) -> None:
    ui.clear()

    for (x, y), t in self.level.tilemap.get_tiles():
      if t.explored:
        t.draw(x + defs.LEVEL_X, y + defs.LEVEL_Y)

    self._rendering.execute(self._entity_list)

    #ui.stats('Health: {} of {}\nTurn: {}'.format(self.player.health.hp, self.player.health.hp_max, self.turn_count))

  def input(self) -> None:
    self._user_input.execute(self._entity_list)

  def update(self) -> None:
    self._turn.execute(self._entity_list)

  def leave(self) -> None:
    pass

  def enter(self) -> None:
    e = ecs.Entity()
    c = components.Player()
    e.add_component(c)
    c = components.Name('Player')
    e.add_component(c)
    c = components.MoveOrAttack()
    e.add_component(c)
    c = components.Position(*self.level.entry)
    e.add_component(c)
    c = components.Graphics('@', ui.WHITE, ui.BLACK, ui.BOLD)
    e.add_component(c)
    c = components.Sight(8)
    e.add_component(c)
    c = components.CombatStats()
    c.ATK = 1
    e.add_component(c)
    self.calc_fov_if_player(e)


    self._entity_list = [e]

    if True:
      rand = rnd.Random()
      for i in range(100):
        x, y = rand.randrange(1, defs.LEVEL_W - 2), rand.randrange(1, defs.LEVEL_H - 2)
        if not self.level.is_blocked(x, y):
          if rand.chance():
            e = monsters.create_orc(x, y)
          else:
            e = monsters.create_snake(x, y)
          self._entity_list.append(e)

    if True:
      rand = rnd.Random()
      for i in range(100):
        x, y = rand.randrange(1, defs.LEVEL_W - 2), rand.randrange(1, defs.LEVEL_H - 2)
        if not self.level.is_blocked(x, y):
          e = items.create_potion_of_healing()
          c = components.Position(x, y)
          e.add_component(c)
          self._entity_list.insert(0, e)


