
import ecs
import components

def name(entity: ecs.Entity, default: str = ''):
    component = entity.get_component(components.Name) # type: components.Name
    if component is not None:
        return component.name
    return default

    

