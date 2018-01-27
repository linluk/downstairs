
import typing

import ui

import ecs
import components

def _basic(name: str, ch: str, fg: int, bg: int) -> ecs.Entity:
  e = ecs.Entity()
  c = components.Name(name)
  e.add_component(c)
  c = components.Graphics(ch, fg, bg)
  e.add_component(c)
  return e

def create_potion_of_healing() -> ecs.Entity:
  return _basic('Potion of Healing', '!', ui.RED, ui.BLACK)

