from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.libtcodpy import console_delete

import color

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap

def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    names = ""
    if game_map.in_bounds(x, y) and game_map.visible[x, y]:
        names += ", ".join(
            entity.name for entity in game_map.entities if entity.x == x and entity.y == y
        )
    return names.capitalize()


def render_bar(
    console: Console, current_value: int, maximum_value: int, total_width: int
) -> None:
    bar_width = int(current_value / maximum_value * total_width)

    console.draw_rect(x=0, y=45, width=20, height=1, ch=1, bg=color.BAR_EMPTY)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.BAR_FILLED
        )
    
    console.print(
        x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=color.BAR_TEXT
    )

def render_names_at_mouse_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )

    console.print(x=x, y=y, string=names_at_mouse_location)