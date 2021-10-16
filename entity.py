from typing import Tuple

class Entity:
    """
    A generic object to represent game entities
    """
    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        self.x, self.y = x, y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy