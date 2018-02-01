
import typing

import ui

import ecs
import components

def create_orc(x: int, y: int) -> ecs.Entity:
  e = ecs.Entity()
  e.add_component(components.Name('Orc'))
  e.add_component(components.MoveOrAttack())
  e.add_component(components.Position(x, y))
  c = components.CombatStats()
  # TODO set some stats
  e.add_component(c)
  e.add_component(components.Blocking())
  e.add_component(components.Graphics('O', ui.GREEN, ui.BLACK))
  return e

def create_snake(x: int, y: int) -> ecs.Entity:
  e = ecs.Entity()
  e.add_component(components.Name('Snake'))
  e.add_component(components.MoveOrAttack())
  e.add_component(components.Position(x, y))
  c = components.CombatStats()
  # TODO set some stats
  e.add_component(c)
  e.add_component(components.Blocking())
  e.add_component(components.Graphics('S', ui.GREEN, ui.BLACK))
  return e

