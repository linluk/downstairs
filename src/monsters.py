
import typing

import ui

import ecs
import components

def create_orc(x: int, y: int) -> ecs.Entity:
  e = ecs.Entity()
  e.add_component(components.Name('Orc'))
  e.add_component(components.Ai(move_or_attack=True))
  e.add_component(components.Position(x, y))
  e.add_component(components.Sight(4))
  c = components.CombatStats()
  c.ATK = 10
  c.DEF = 10
  c.HPM = 1
  c.HP = c.HPM
  e.add_component(c)
  e.add_component(components.Blocking())
  e.add_component(components.Graphics('O', ui.GREEN, ui.BLACK))
  return e

def create_snake(x: int, y: int) -> ecs.Entity:
  e = ecs.Entity()
  e.add_component(components.Name('Snake'))
  e.add_component(components.Ai(move_or_attack=True))
  e.add_component(components.Position(x, y))
  e.add_component(components.Sight(4))
  c = components.CombatStats()
  c.ATK = 10
  c.DEF = 10
  c.HPM = 1
  c.HP = c.HPM
  e.add_component(c)
  e.add_component(components.Blocking())
  e.add_component(components.Graphics('S', ui.GREEN, ui.BLACK))
  return e

