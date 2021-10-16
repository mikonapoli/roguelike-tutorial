from __future__ import annotations

import random
from typing import Iterator, Tuple, List, TYPE_CHECKING

from game_map import GameMap
import tile_types

import tcod

if TYPE_CHECKING:
    from entity import Entity


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x1, self.y1 = x, y
        self.x2, self.y2 = x + width, y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """
        Return the inner area of this room as a 2D array index.
        """
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom):
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def generate_dungeon(max_rooms: int, 
room_min_size: int,
room_max_size: int,
map_width: int,
map_height: int,
player: Entity) -> GameMap:

    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangularRoom] = []

    for _ in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height -1)
        new_room = RectangularRoom(x, y ,room_width, room_height)
        if all([not new_room.intersects(room) for room in rooms]):
            rooms.append(new_room)
            dungeon.tiles[new_room.inner] = tile_types.floor
    
    player.x, player.y = rooms[0].center


    for i, room in enumerate(rooms[1:]):
        for x, y in tunnel_between(rooms[i].center, room.center):
            dungeon.tiles[x, y] = tile_types.floor      

    return dungeon

def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """
    Return an L-Shaped tunnel between these two points
    """
    x1, y1 = start
    x2, y2 = end
    
    corner_x, corner_y = (x2, y1) if random.random() < .5 else (x1, y2)

    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)):
        yield x, y

    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)):
        yield x, y
