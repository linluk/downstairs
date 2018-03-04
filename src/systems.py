
from typing import Set, Callable, Iterable

import ecs
import rnd

import ui
import ui.commands
from ui.commands import Commands
import components

import gameover

import utils
import defs
import level
import state_manager
import inventory

class BaseSystem(ecs.System): # {{{1
  """ base class for game systems (game dependencies i dont want to have in the ecs module) """
  def __init__(self, relevant_components: Iterable[ecs.ComponentType], iterate_copy: bool = False) -> None:
    super().__init__(relevant_components, iterate_copy)
    self._level = None # type: level.Level
    self._state_manager = None # type: state_manager.StateManager

  def execute(self, level_: level.Level, state_manager_: state_manager.StateManager, entities: Set[ecs.Entity]):
    self._level = level_
    self._state_manager = state_manager_
    super().execute(entities)

  level = property(lambda s: s._level)
  state_manager = property(lambda s: s._state_manager)



class UserInput(BaseSystem):  # {{{1
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
    elif cmd == Commands.TAKE:
      entity.add_component(components.Action(take=True))
    elif cmd == Commands.INVENTORY:
      self.state_manager.change_state(inventory.Inventory)
      self.state_manager.next.set_items(entity.get_component(components.Items))
    else:
      ui.message('command not implemented!')

  on_quit = property(_get_on_quit, _set_on_quit)

class Ai(BaseSystem):  # {{{1
  def __init__(self) -> None:
    super().__init__([components.Ai])
    self._line_of_sight = None
    self.p_position = None # type: components.Position
    self.p_combat_stats = None # type: components.CombatStats


  def _can_see(self, r: float, x1: int, y1: int, x2: int, y2: int) -> bool:
    if ((max(x1, x2) - min(x1, x2))**2 + (max(y1, y2) - min(y1, y2))**2)**0.5 > r:
      return False
    if self._line_of_sight is not None:
      return self._line_of_sight(x1, y1, x2, y2)
    else:
      return False
  def _set_line_of_sight(self, line_of_sight: Callable[[int, int, int, int], bool]) -> None:
    self._line_of_sight = line_of_sight

  def before(self, entities: Set[ecs.Entity]) -> bool:
    p = None # type: ecs.Entity
    for e in entities:
      if e.has_component(components.Player):
        p = e
        break

    if p is not None:
      self.p_position = p.get_component(components.Position) # type: components.Position
      self.p_combat_stats = p.get_component(components.CombatStats) # type: components.CombatStats

    return super().before(entities)


  def update(self, entity: ecs.Entity, entities: Set[ecs.Entity]):
    ai = entity.get_component(components.Ai) # type: components.Ai
    if ai.move_or_attack:
      position = entity.get_component(components.Position) # type: components.Position
      if position is not None:
        move_or_attack = entity.get_component(components.MoveOrAttack) # type: components.MoveOrAttack
        if move_or_attack is None:
          move_or_attack = components.MoveOrAttack()
          entity.add_component(move_or_attack)
        moved = False
        sight = entity.get_component(components.Sight) # type: components.Sight
        if sight is not None:
          if self._can_see(sight.radius, position.x, position.y, self.p_position.x, self.p_position.y):
            ui.message('{} sees player'.format(hash(entity)))
            move_or_attack.dx = 1 if position.x < self.p_position.x else -1 if position.x > self.p_position.x else 0
            move_or_attack.dy = 1 if position.y < self.p_position.y else -1 if position.y > self.p_position.y else 0
            moved = True
        if not moved:
          move_or_attack.dx = rnd.randrange(-2, 2)
          move_or_attack.dy = rnd.randrange(-2, 2)
    #print(str(move_or_attack))

  line_of_sight = property(lambda s: s._line_of_sight, _set_line_of_sight)



class Turn(BaseSystem):  # {{{1
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
      p = e.get_component(components.Position) # type: components.Position
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

  def _take(self, entity: ecs.Entity, entities: Set[ecs.Entity]) -> None:
    action = entity.get_component(components.Action)
    if not action.take:
      return
    entity.remove_component(components.Action)
    items = entity.get_component(components.Items) # type: components.Items
    position = entity.get_component(components.Position)
    candidates = [e for e in self.entities_at_position(position.x, position.y, entities) if e.has_component(components.Weight)]
    if len(candidates) > 0:
      # TODO: wenn mehr als ein candidate fragen welcher aufgenommen werden soll
      item = candidates[0]
      item.remove_component(components.Position)
      items.items.append(item)



  def _move_or_attack(self, entity: ecs.Entity, entities: Set[ecs.Entity]) -> None:
    position = entity.get_component(components.Position) # type: components.Position
    move_or_attack = entity.get_component(components.MoveOrAttack) # type: components.MoveOrAttack
    # No need to check if move_or_attack is not None because Turn.update() only
    # iterates over entities having a MoveOrAttack Component
    cx = position.x + move_or_attack.dx
    cy = position.y + move_or_attack.dy
    combat_stats = entity.get_component(components.CombatStats) # type: components.CombatStats
    if combat_stats is not None:
      for e in iter(e for e in self.entities_at_position(cx, cy, entities) if e != entity):
        other_combat_stats = e.get_component(components.CombatStats) # type: components.CombatStats
        if other_combat_stats is not None:
          # now we have our (whoever it is) and others combat stats

          # http://www.roguebasin.com/index.php?title=Thoughts_on_Combat_Models
          # TODO: this does not work yet!!!
          hit = rnd.random() > combat_stats.ATK / (combat_stats.ATK + other_combat_stats.DEF)
          if hit:
            damage = max(1, rnd.random() * (combat_stats.ATK - other_combat_stats.DEF))
            other_combat_stats.HP -= damage

            if other_combat_stats.HP <= 0:
              if e.has_component(components.Player):
                self.state_manager.add_state(gameover.Gameover()) # TODO: alles mögliche zur anzeige im game over screen übergeben
                self.state_manager.change_state(gameover.Gameover)
              else:
                corpse = ecs.Entity()
                corpse.add_component(components.Position(cx, cy))
                corpse.add_component(components.Graphics('%', ui.RED, st=ui.BOLD))
                corpse.add_component(components.Weight(1))
                corpse.add_component(components.Name('{} {}'.format(utils.name(e), 'Corpse').strip()))
                entities.insert(1, corpse) # insert, not append, to draw early
                entities.remove(e)
                ui.message('{} killed {}'.format(hash(entity), hash(e)))
            else:
              ui.message('{} did {} damage to {}'.format(hash(entity), damage, hash(e)))
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
    self._call_sub(self._take, [components.Action, components.Items, components.Position])

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

class Rendering(BaseSystem):  # {{{1

  def __init__(self, offset_x: int = 0, offset_y: int = 0) -> None:
    super().__init__([components.Graphics, components.Position])
    self._check_visible = None # type: Callable[[int, int], bool]
    self._offset_x = offset_x
    self._offset_y = offset_y

  def before(self, entities: Set[ecs.Entity]) -> bool:
    ui.clear()

    for (x, y), t in self.level.tilemap.get_tiles():
      if t.explored:
        t.draw(x + defs.LEVEL_X, y + defs.LEVEL_Y)

    return super().before(entities)

  def update(self, entity: ecs.Entity, entities: Set[ecs.Entity]) -> None:
    position = entity.get_component(components.Position)
    # i do not need to check if position is assigned. i only get entities who has a Position Component.
    if self._do_check_visible(position.x, position.y):
      g = entity.get_component(components.Graphics)
      # i do not need to check if g is assigned. i only get entities who has a Graphics Component.
      ui.addch(position.x + self._offset_x, position.y + self._offset_y, g.ch, g.fg, g.bg, g.st)

    player = entity.get_component(components.Player)
    if player is not None:
      combat_stats = entity.get_component(components.CombatStats) # type: components.CombatStats
      if combat_stats is not None:
        ui.stats(' HP: {:3}  HPM: {:3}\nATK: {:3}  DEF: {:3}'.format(combat_stats.HP, combat_stats.HPM, combat_stats.ATK, combat_stats.DEF))



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

