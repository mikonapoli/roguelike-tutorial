from typing import Tuple

import numpy as np  # type: ignore


graphic_dt = np.dtype([("ch", np.int32), ("fg", "3B"), ("bg", "3B")])

tile_dt = np.dtype(
    [("walkable", np.bool), ("transparent", np.bool), ("dark", graphic_dt), ("light", graphic_dt)]
)


def new_tile(
    *,
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
    """Helper function for creating defining individual tile types"""
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


floor = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (25, 25, 125)),
    light=(ord(" "), (255, 255, 255), (75, 75, 175))
)
wall = new_tile(
    walkable=False, transparent=False, dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (100, 100, 200))
)

SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)