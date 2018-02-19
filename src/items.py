
import typing

import ui

import ecs
import components

def _basic(name: str, weight: float,  ch: str, fg: int, bg: int) -> ecs.Entity:
  e = ecs.Entity()
  e.add_component(components.Name(name))
  e.add_component(components.Graphics(ch, fg, bg))
  e.add_component(components.Weight(weight))
  return e

def create_potion_of_healing() -> ecs.Entity:
  return _basic('Potion of Healing', 1.0, '!', ui.RED, ui.BLACK)

