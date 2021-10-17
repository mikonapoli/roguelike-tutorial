from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import color

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """
        Perform this action with the objects needed to deterimne its scope
        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx, self.dy = dx, dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        return self.engine.game_map.get_blocking_entities(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()

class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if target is not None:
            damage = self.entity.fighter.power - target.fighter.defense
            description = f"{self.entity.name} attacks {target.name}"

            attack_color = color.PLAYER_ATK if self.entity is self.engine.player else color.ENEMY_ATK
            if damage > 0:
                self.engine.message_log.add_message(f"{description} for {damage} hit points.", attack_color)
                target.fighter.hp -= damage
            else:
                self.engine.message_log.add_message(f"{description} but deals no damage", attack_color)

class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if target is not None:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()

class MovementAction(ActionWithDirection):

    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        movable = (
            self.engine.game_map.in_bounds(dest_x, dest_y)
            and self.engine.game_map.tiles["walkable"][dest_x, dest_y]
            and self.engine.game_map.get_blocking_entities(dest_x, dest_y) is None
        )

        if movable:
           self.entity.move(self.dx, self.dy)

class WaitAction(Action):
    def perform(self) -> None:
        pass
