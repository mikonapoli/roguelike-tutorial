from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from action import Action, EscapeAction, BumpAction, WaitAction

if TYPE_CHECKING:
    from engine import Engine

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def handle_events(self) -> None:
        raise NotImplementedError()
    
    def ev_quit(self, event: tcod.event.Quit) -> None:
        raise SystemExit()

    


class MainGameEventHandler(EventHandler):
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)            
            if action is not None:
                action.perform()
                self.engine.handle_enemy_turns()
                self.engine.update_fov()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:

        key = event.sym
        player = self.engine.player

        MOVE_KEYS = {
            tcod.event.K_UP: (0, -1),
            tcod.event.K_DOWN: (0, 1),
            tcod.event.K_LEFT: (-1, 0),
            tcod.event.K_RIGHT: (1, 0),
            tcod.event.K_HOME: (-1, -1),
            tcod.event.K_END: (-1, 1),
            tcod.event.K_PAGEUP: (1, -1),
            tcod.event.K_PAGEDOWN: (1, 1),
            tcod.event.K_k: (0, -1),
            tcod.event.K_j: (0, 1),
            tcod.event.K_h: (-1, 0),
            tcod.event.K_l: (1, 0),
            tcod.event.K_y: (-1, -1),
            tcod.event.K_b: (-1, 1),
            tcod.event.K_u: (1, -1),
            tcod.event.K_n: (1, 1),
        }

        WAIT_KEYS = {tcod.event.K_PERIOD, tcod.event.K_KP_5, tcod.event.K_CLEAR}

        actions = {k: BumpAction(player, *v) for k, v in MOVE_KEYS.items()}
        for k in WAIT_KEYS:
            actions[k] = WaitAction(player)
        actions[tcod.event.K_ESCAPE] = EscapeAction(player)

        action: Optional[Action] = actions.get(key, None)
        return action


class GameOverEventHandler(EventHandler):
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is not None:
                action.perform()
    
    def ev_keydown(self, event: "tcod.event.KeyDown") -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym
        if key == tcod.event.K_ESCAPE:
            action = EscapeAction(self.engine.player)
        return action