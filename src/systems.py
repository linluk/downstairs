
from typing import Set, Callable, Iterable

import ecs

import ui
import ui.commands
from ui.commands import Commands
import components

class UserInput(ecs.System):  # {{{
  def __init__(self):
    super().__init__([components.Player])
    self._on_quit = None # type: Callable[[], None]

  def _do_on_quit(self) -> None:
    if self._on_quit is not None:
      self._on_quit()
  def _get_on_quit(self) -> Callable[[], None]:
    return self._on_quit
  def _set_on_quit(self, on_quit: Callable[[], None]) -> None:
    self._on_quit = on_quit

  def update(self, entity: ecs.Entity, _unused) -> None:
    cmd = ui.commands.getcmd()
    if cmd.is_direction():
      move_or_attack = entity.get_component(components.MoveOrAttack)
      if move_or_attack is None:
        move_or_attack = components.MoveOrAttack()
        entity.add_component(move_or_attack)
      move_or_attack.dxdy = cmd.direction_to_dxdy()
    elif cmd == Commands.QUIT:
      self._do_on_quit()
    elif cmd == Commands.OPEN:
      ui.message('which direction?')
      direction = ui.commands.require_direction()
      if direction is not None:
        dx, dy = direction.direction_to_dxdy()
        position = entity.get_component(components.Position)
        if position is not None:
          door = entity.get_component(components.Door)
          if door is None:
            door = components.Door()
            entity.add_component(door)
          door.xy = (position.x + dx, position.y + dy)
    return None


    if cmd == Commands.SKIP: turn = True
    elif cmd == Commands.ATTACK:
      ui.message('which direction?')
      direction = ui.commands.require_direction()
      if direction is not None:
        x, y = direction.direction_to_dxdy()
        turn = self.player.combat.attack_xy(self.player.position.x + x, self.player.position.y + y)

    else:
      ui.message('command not implemented!')

  on_quit = property(_get_on_quit, _set_on_quit)
# }}}


class Turn(ecs.System):  # {{{
  def __init__(self):
    super().__init__([], True)
    self._check_blocked = None # type: Callable[[int, int], bool]
    self._on_moved = None # type: Callable[[ecs.Entity], None]
    self._toggle_door = None # type Callable[[ecs.Entity, int, int], bool]
    self._current_entity = None # type: ecs.Entity
    self._current_entities = None # type: Set[ecs.Entity]


  def is_blocked(self, x: int, y: int, entities: Set[ecs.Entity] = None) -> bool:
    if self._do_check_blocked(x, y):
      return True
    for e in self.entities_at_position(x, y, entities):
      b = e.get_component(components.Blocking)
      if b is not None:
        if b.value:
          return True
    return False

  def entities_at_position(self, x: int, y: int, entities: Set[ecs.Entity]) -> Iterable[ecs.Entity]:
    for e in entities:
      p = e.get_component(components.Position) # type: component.Position
      if p is not None:
        if p.x == x and p.y == y:
          yield e

  def _call_sub(self, method: Callable[[ecs.Entity, Set[ecs.Entity]], None], required_components: Iterable[ecs.ComponentType]) -> None:
    entity = self._current_entity
    relevant_entity = True
    for required_component in required_components:
      if not entity.has_component(required_component):
        relevant_entity = False
        break
    if relevant_entity:
      method(entity, self._current_entities)

  def _move_or_attack(self, entity: ecs.Entity, entities: Set[ecs.Entity]) -> None:
    position = entity.get_component(components.Position) # type: components.Position
    move_or_attack = entity.get_component(components.MoveOrAttack) # type: components.MoveOrAttack
    # No need to check if move_or_attack is not None because Turn.update() only
    # iterates over entities having a MoveOrAttack Component
    cx = position.x + move_or_attack.dx
    cy = position.y + move_or_attack.dy
    combat_stats = entity.get_component(components.CombatStats) # type: components.CombatStats
    if combat_stats is not None:
      for e in self.entities_at_position(cx, cy, entities):
        other_combat_stats = e.get_component(components.CombatStats) # type: components.CombatStats
        if other_combat_stats is not None:
          other_combat_stats.HP -= combat_stats.ATK
          if other_combat_stats.HP <= 0:
            entities.remove(e)
            ui.message('{} killed {}'.format(hash(entity), hash(e)))
          return ### refactor but if we are here no moving should be done!!

    if not self.is_blocked(cx, cy, entities):
      position.xy = (cx, cy)
      self._do_on_moved(entity)
      # TODO: if i am the player count it a a turn
    entity.remove_component(components.MoveOrAttack)
    #move_or_attack.dxdy = (0, 0)

  def _open_or_close_door(self, entity: ecs.Entity, entities: Set[ecs.Entity]) -> None:
    door = entity.get_component(components.Door)
    self._do_toggle_door(entity, door.x, door.y)
    # TODO if this returned true (the door has been toggled) this should be a turn if the entity has a Player component
    entity.remove_component(components.Door)

  def update(self, entity: ecs.Entity, entities: Set[ecs.Entity]) -> None:
    self._current_entity = entity
    self._current_entities = entities
    self._call_sub(self._move_or_attack, [components.Position, components.MoveOrAttack])
    self._call_sub(self._open_or_close_door, [components.Door])

  def _do_on_moved(self, entity: ecs.Entity) -> None:
    if self._on_moved is not None:
      self._on_moved(entity)
  def _get_on_moved(self) -> Callable[[ecs.Entity], None]:
    return self._do_on_moved
  def _set_on_moved(self, on_moved: Callable[[ecs.Entity], None]) -> None:
    self._on_moved = on_moved

  def _do_check_blocked(self, x: int, y: int) -> bool:
    if self._check_blocked is not None:
      return self._check_blocked(x, y)
    else:
      return False
  def _get_check_blocked(self):
    return self._check_blocked
  def _set_check_blocked(self, check_blocked) -> None:
    self._check_blocked = check_blocked

  def _do_toggle_door(self, entity: ecs.Entity, x: int, y: int) -> bool:
    if self._toggle_door is not None:
      return self._toggle_door(entity, x, y)
    return False
  def _get_toggle_door(self) -> Callable[[ecs.Entity, int, int], bool]:
    return self._toggle_door
  def _set_toggle_door(self, toggle_door: Callable[[ecs.Entity, int, int], bool]) -> None:
    self._toggle_door = toggle_door

  toggle_door = property(_get_toggle_door, _set_toggle_door, doc='should return true when toggled the door')
  check_blocked = property(_get_check_blocked, _set_check_blocked)
  on_moved = property(_get_on_moved, _set_on_moved)
# }}}

class Rendering(ecs.System):  # {{{

  def __init__(self, offset_x: int = 0, offset_y: int = 0) -> None:
    super().__init__([components.Graphics, components.Position])
    self._check_visible = None # type: Callable[[int, int], bool]
    self._offset_x = offset_x
    self._offset_y = offset_y

  def update(self, entity: ecs.Entity, entities: Set[ecs.Entity]) -> None:
    p = entity.get_component(components.Position)
    # i do not need to check if p is assigned. i only get entities who has a Position Component.
    if self._do_check_visible(p.x, p.y):
      g = entity.get_component(components.Graphics)
      # i do not need to check if g is assigned. i only get entities who has a Graphics Component.
      ui.addch(p.x + self._offset_x, p.y + self._offset_y, g.ch, g.fg, g.bg, g.st)

  def _do_check_visible(self, x: int, y: int) -> bool:
    if self._check_visible is not None:
      return self._check_visible(x, y)
    else:
      return False
  def _get_check_visible(self):
    return self._check_visible
  def _set_check_visible(self, check_visible) -> None:
    self._check_visible = check_visible

  check_visible = property(_get_check_visible, _set_check_visible)

# }}}
