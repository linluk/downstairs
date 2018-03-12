
import ecs

import systems_base

import components

class MoveOrAttack(systems_base.BaseSubSystem):
    def __init__(self, parent: systems_base.BaseSystem,):
        super().__init__(parent, [components.Position, components.Moveable])

    def update(self, entity: ecs.Entity, entities: Set[ecs.Entity]):
        pass

