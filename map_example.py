from numba.core import types
from numba.typed import Dict
from numba import int32
from map_edit import *
import pygame

tile = 100
WORLD_WIDTH, WORLD_HEIGHT = max([len(i) for i in matrix_map]) * tile, len(matrix_map) * tile
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
collision_walls = []
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            collision_walls.append(pygame.Rect(i * tile, j * tile, tile, tile))
            if char == 1:
                world_map[(i * tile, j * tile)] = 1