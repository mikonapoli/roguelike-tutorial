import tcod
from action import EscapeAction, MovementAction

from event_handler import EventHandler

tileset_file = "assets/dejavu10x10_gs_tc.png"

def main() -> None:
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width // 2)
    player_y = int(screen_height // 2)

    tileset = tcod.tileset.load_tilesheet(
        tileset_file, 32, 8, tcod.tileset.CHARMAP_TCOD
        )

    event_handler = EventHandler()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.print(x=player_x, y=player_y, string="@")

            context.present(root_console)
            
            root_console.clear()

            for event in tcod.event.wait():
                action = event_handler.dispatch(event)

            if isinstance(action, MovementAction):
                player_x += action.dx
                player_y += action.dy
            
            elif isinstance(action, EscapeAction):
                raise SystemExit()

    print("All good")

if __name__ == "__main__":
    main()