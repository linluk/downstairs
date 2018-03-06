
import ui
import ui.commands
from ui.commands import Commands
import tilemap
import defs



import world

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
    self.world = world.World()

    self._entity_list = []

    self._user_input = systems.UserInput()
    self._user_input.on_quit = self.quit

    self._turn = systems.Turn()
    self._turn.check_blocked = self.world.current.is_blocked ## TODO : fix for world
    self._turn.on_moved = self.moved
    self._turn.toggle_door = self.toggle_door

    self._ai = systems.Ai()
    self._ai.line_of_sight = self.line_of_sight

    self._rendering = systems.Rendering(defs.LEVEL_X, defs.LEVEL_Y)
    self._rendering.check_visible = self.world.current.is_visible ## TODO : fix for world

  def line_of_sight(self, x1: int, y1: int, x2: int, y2: int) -> bool:
      return self.world.current.tilemap.los(x1, y1, x2, y2) ## TODO : fix for world

  def calc_fov_if_player(self, entity: ecs.Entity):
    if entity.has_component(components.Player):
      sight = entity.get_component(components.Sight) # type: components.Sight
      self.world.current.tilemap.fov(*entity.get_component(components.Position).xy, sight.radius) ## TODO : fix for world


  def quit(self):
    #self.state_manager.terminate_main_loop()
    self.state_manager.change_state(menu.Menu)

  def moved(self, entity: ecs.Entity):
    self.calc_fov_if_player(entity)

  def toggle_door(self, entity, x, y):
    t = self.world.current.tilemap.get_tile(x, y) ## TODO : fix for world
    if isinstance(t, tilemap.Door):
      t.toggle()
      self.calc_fov_if_player(entity)
      return True
    return False

  def render(self) -> None:
      self._rendering.execute(self.world, self.state_manager, self._entity_list)


  def input(self) -> None:
      self._user_input.execute(self.world, self.state_manager, self._entity_list)

  def update(self) -> None:
    self._ai.execute(self.world, self.state_manager, self._entity_list)
    self._turn.execute(self.world, self.state_manager, self._entity_list)

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
    c = components.Position(*self.world.current.entry) ## TODO : fix for world
    e.add_component(c)
    c = components.Graphics('@', ui.WHITE, ui.BLACK, ui.BOLD)
    e.add_component(c)
    c = components.Sight(8)
    e.add_component(c)
    c = components.CombatStats()
    c.ATK = 10
    c.DEF = 10
    c.HPM = 25
    c.HP = c.HPM
    e.add_component(c)
    e.add_component(components.Items())
    self.calc_fov_if_player(e)

    self._entity_list = [e]

    if True:
      rand = rnd.Random()
      for i in range(100):
        x, y = rand.randrange(1, defs.LEVEL_W - 2), rand.randrange(1, defs.LEVEL_H - 2)
        if not self.world.current.is_blocked(x, y): ## TODO : fix for world
          if rand.chance():
            e = monsters.create_orc(x, y)
          else:
            e = monsters.create_snake(x, y)
          self._entity_list.append(e)

    if True:
      rand = rnd.Random()
      for i in range(100):
        x, y = rand.randrange(1, defs.LEVEL_W - 2), rand.randrange(1, defs.LEVEL_H - 2)
        if not self.world.current.is_blocked(x, y): ## TODO : fix for world
          e = items.create_potion_of_healing()
          c = components.Position(x, y)
          e.add_component(c)
          self._entity_list.insert(0, e)


