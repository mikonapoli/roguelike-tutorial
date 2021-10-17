from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from action import Action, EscapeAction, BumpAction

if TYPE_CHECKING:
    from engine import Engine


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

        if action is not None:
            action.perform()
            self.engine.handle_enemy_turns()
            self.engine.update_fov()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:

        key = event.sym
        player = self.engine.player

        keymap = {
            tcod.event.K_UP: BumpAction(player, dx=0, dy=-1),
            tcod.event.K_DOWN: BumpAction(player, dx=0, dy=1),
            tcod.event.K_LEFT: BumpAction(player, dx=-1, dy=0),
            tcod.event.K_RIGHT: BumpAction(player, dx=1, dy=0),
            tcod.event.K_ESCAPE: EscapeAction(player)
        }

        action: Optional[Action] = keymap.get(key, None)

        return action