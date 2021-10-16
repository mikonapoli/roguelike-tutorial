from __future__ import annotations

import copy

from typing import Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent game entities
    """

    def __init__(self, 
    x: int = 0, 
    y: int = 0, 
    char: str = "?", 
    color: Tuple[int, int, int] = (255, 255, 255),
    name: str = "<Unnamed>",
    blocks_movement: bool = False):
        self.x, self.y = x, y
        self.char = char
        self.color = color
        self.name = name
        self.blcoks_movement = blocks_movement

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        gamemap.entities.add(clone)
        return clone


    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
