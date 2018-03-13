
from typing import Set, Iterable

import ecs
import components
import world

def name(entity: ecs.Entity, default: str = ''):
    component = entity.get_component(components.Name) # type: components.Name
    if component is not None:
        return component.name
    return default

def entities_at_position(x: int, y: int, entities: Set[ecs.Entity]) -> Iterable[ecs.Entity]:
    for e in entities:
        p = e.get_component(components.Position) # type: components.Position
        if p is not None:
            if p.x == x and p.y == y:
                yield e

def is_blocked(x: int, y: int, world: world.World, entities: Set[ecs.Entity] = None) -> bool:
    if world.current.is_blocked(x, y):
        return True
    for e in entities_at_position(x, y, entities):
        b = e.get_component(components.Blocking)
        if b is not None:
            if b.value:
                return True
    return False
