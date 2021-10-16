import tcod
from engine import Engine
from entity import Entity
from game_map import GameMap

from event_handler import EventHandler

tileset_file = "assets/dejavu10x10_gs_tc.png"


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    tileset = tcod.tileset.load_tilesheet(
        tileset_file, 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player_x = int(screen_width // 2)
    player_y = int(screen_height // 2)

    player = Entity(player_x, player_y, "@", (255, 255, 255))
    npc = Entity(player_x - 5, player_y, "@", (255, 255, 0))
    entities = {npc, player}

    game_map = GameMap(map_width, map_height)

    engine = Engine(
        entities=entities, event_handler=event_handler, game_map=game_map, player=player
    )

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")

        while True:
            engine.render(console=root_console, context=context)
            events = tcod.event.wait()
            engine.handle_events(events)

    print("All good")


if __name__ == "__main__":
    main()
