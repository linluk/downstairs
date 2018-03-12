
from typing import Iterable, Set

import ecs

import components
import world
import state_manager



class BaseSystem(ecs.System): # {{{1
    """ base class for game systems (game dependencies i dont want to have in the ecs module) """
    def __init__(self, required_components: Iterable[ecs.ComponentType], iterate_copy: bool = False) -> None:
        super().__init__(required_components, iterate_copy)
        self._world = None # type: world.World
        self._state_manager = None # type: state_manager.StateManager

    def execute(self, world_: world.World, state_manager_: state_manager.StateManager, entities: Set[ecs.Entity]):
        self._world = world_
        self._state_manager = state_manager_
        super().execute(entities)

    world = property(lambda s: s._world)
    state_manager = property(lambda s: s._state_manager)


class BaseSubSystem(object): # {{{1
    """ base class for subsystems. a subsystem can be used by a system and called to a single entity. it does not iterate over entities. """
    def __init__(self, parent_system: BaseSystem, required_components: Iterable[ecs.ComponentType]):
        super().__init__()
        self._parent = parent_system
        self._entities = None # type : Set[ecs.Entity]
        self._required_components = set(required_components)

    def update(self, entity: ecs.Entity, entities: Set[ecs.Entity]):
        pass

    def execute(self, entity: ecs.Entity):
        relevant_entity = True
        for required_component in self._required_components:
            if not entity.has_component(required_component):
                relevant_entity = False
                break
        if relevant_entity:
            self.update(entity, self._entities)

    def _set_entities(self, entities: Set[ecs.Entity]):
        self._entities = entities

    parent = property(lambda s: s._parent)
    entities = property(lambda s: s._entities, _set_entities)


