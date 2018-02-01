

from typing import Iterable, Set, Type


class Component(object):
  def __init__(self):
    super().__init__()


ComponentType = Type[Component]



__global_next_id = 1 # type: int
def _next_id() -> int:
  global __global_next_id
  i = __global_next_id
  __global_next_id += 1
  return i

class Entity(object):
  __slots__ = ('_id', '_components')
  def __init__(self):
    super().__init__()
    self._id = _next_id()
    self._components = {} # type: Dict[ComponentTypes, Component]

  def add_component(self, component: Component) -> None:
    self._components[type(component)] = component

  def has_component(self, component_type: ComponentType) -> bool:
    return component_type in self._components

  def remove_component(self, component_type: ComponentType) -> None:
    if component_type in self._components:
      del self._components[component_type]

  def get_component(self, component_type: ComponentType) -> Component:
    return self._components.get(component_type, None)

  def __hash__(self):
    return self._id

  def __eq__(self, other):
    return self._id == hash(other)


class System(object):
  __slots__ = ('_relevant_components', '_prepare_for_iteration')
  def __init__(self, relevant_components: Iterable[ComponentType], iterate_copy: bool = False) -> None:
    super().__init__()
    self._relevant_components = set(relevant_components) # type: Set[ComponentType]
    if iterate_copy:
      self._prepare_for_iteration = lambda x: x.copy()
    else:
      self._prepare_for_iteration = lambda x: x

  def update(self, entity: Entity, entities: Set[Entity]):
    pass

  def before(self, entities: Set[Entity]) -> bool:
    return True

  def after(self, entities: Set[Entity]):
    pass

  def execute(self, entities: Set[Entity]):
    prepared_entities = self._prepare_for_iteration(entities)
    if self.before(prepared_entities):
      for entity in prepared_entities:
        relevant_entity = True
        for relevant_component in self._relevant_components:
          if not entity.has_component(relevant_component):
            relevant_entity = False
            break
        if relevant_entity:
          self.update(entity, entities)
    self.after(prepared_entities)


