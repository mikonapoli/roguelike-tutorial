from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Perform this action with the objects needed to deterimne its scope
        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


class ActionWithDirection(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx, self.dy = dx, dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()

class MeleeAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        target = engine.game_map.get_blocking_entities(dest_x, dest_y)
        if target is not None:
            print(f"You kick the {target.name} much to its annoyance")

class BumpAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        target = engine.game_map.get_blocking_entities(dest_x, dest_y)
        if target is not None:
            return MeleeAction(self.dx, self.dy).perform(engine, entity)
        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)

class MovementAction(ActionWithDirection):
    def __init__(self, dx: int, dy: int):
        super().__init__(dx, dy)

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        movable = (
            engine.game_map.in_bounds(dest_x, dest_y)
            and engine.game_map.tiles["walkable"][dest_x, dest_y]
            and engine.game_map.get_blocking_entities(dest_x, dest_y) is None
        )

        if movable:
            entity.move(self.dx, self.dy)
