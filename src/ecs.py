

from typing import Iterable, Set, Type


class Component(object):

  def __init__(self):
    super().__init__()



ComponentType = Type[Component]
RegisteredComponentTypes: Set[ComponentType] = set()

def register_component(component_type: ComponentType):
    global RegisteredComponentTypes
    RegisteredComponentTypes.add(component_type)


class Entity(object):

    __slots__ = ('_id', '_components')

    __next_id: int = 1
    @classmethod
    def _next_id(cls) -> int:
        i = cls.__next_id
        cls.__next_id += 1
        return i

    def __init__(self):
        super().__init__()
        self._id = self.__class__._next_id()
        self._components: Dict[ComponentTypes, Component] = {}

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
        self._relevant_components: Set[ComponentType] = set(relevant_components)
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


