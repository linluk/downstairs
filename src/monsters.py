
import typing

import ui

import ecs
import components

def create_orc(x: int, y: int) -> ecs.Entity:
  e = ecs.Entity()
  c = components.Name('Orc')
  e.add_component(c)
  c = components.MoveOrAttack()
  e.add_component(c)
  c = components.Position(x, y)
  e.add_component(c)
  c = components.CombatStats()
  # TODO set some stats
  e.add_component(c)
  c = components.Blocking()
  e.add_component(c)
  c = components.Graphics('O', ui.GREEN, ui.BLACK)
  e.add_component(c)
  return e

def create_snake(x: int, y: int) -> ecs.Entity:
  e = ecs.Entity()
  c = components.Name('Snake')
  e.add_component(c)
  c = components.MoveOrAttack()
  e.add_component(c)
  c = components.Position(x, y)
  e.add_component(c)
  c = components.CombatStats()
  # TODO set some stats
  e.add_component(c)
  c = components.Blocking()
  e.add_component(c)
  c = components.Graphics('S', ui.GREEN, ui.BLACK)
  e.add_component(c)
  return e

