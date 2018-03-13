
# stdlib
from typing import Set

# clean
import ecs
import rnd

# ugly
import ui
import gameover

# required
import systems_base
import components
import utils


class MoveOrAttack(systems_base.BaseSubSystem):
    def __init__(self, parent: systems_base.BaseSystem,):
        super().__init__(parent, [components.Position, components.Moveable])

    def update(self, entity: ecs.Entity, entities: Set[ecs.Entity], dx: int, dy: int):
        position = entity.get_component(components.Position) # type: components.Position
        # No need to check if move_or_attack is not None because Turn.update() only
        # iterates over entities having a MoveOrAttack Component
        cx = position.x + dx
        cy = position.y + dy
        combat_stats = entity.get_component(components.CombatStats) # type: components.CombatStats
        if combat_stats is not None:
            other_combat_stats = None
            for e in iter(e for e in utils.entities_at_position(cx, cy, entities) if e != entity):
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

        if not utils.is_blocked(cx, cy, self.world, entities):
            position.xy = (cx, cy)
            if entity.has_component(components.Player):
                sight = entity.get_component(components.Sight) # type: components.Sight
                self.world.current.tilemap.fov(*entity.get_component(components.Position).xy, sight.radius)
            #self._do_on_moved(entity)
            # TODO: if i am the player count it a a turn
        #entity.remove_component(components.MoveOrAttack)
        #move_or_attack.dxdy = (0, 0)

