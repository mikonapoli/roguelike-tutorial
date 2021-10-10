from typing import Optional

import tcod.event

from action import Action, EscapeAction, MovementAction


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:

        key = event.sym

        keymap = {
            tcod.event.K_UP: MovementAction(dx=0, dy=-1),
            tcod.event.K_DOWN: MovementAction(dx=0, dy=1),
            tcod.event.K_LEFT: MovementAction(dx=-1, dy=0),
            tcod.event.K_RIGHT: MovementAction(dx=1, dy=0),
            tcod.event.K_ESCAPE: EscapeAction()
        }

        action: Optional[Action] = keymap.get(key, None)

        return action