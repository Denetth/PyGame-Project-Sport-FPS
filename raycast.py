import pygame
from settings import *
from map_example import world_map, WORLD_WIDTH, WORLD_HEIGHT
from numba import njit

num_of_rays = 300
scaling = WIDTH // 300
fov = math.pi / 3
projection_coeff = 3 * (300 / (2 * math.tan((math.pi / 3) / 2))) * 100
delta = (math.pi / 3) / 300


@njit(fastmath=True, cache=True)
def mapping(a, b):
    return int((a // 100) * 100), int((b // 100) * 100)


@njit(fastmath=True, cache=True)
def raycasting(player_pos, player_angle, world_map):
    casted_walls = []
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - (fov / 2)
    texture_v, texture_h = 1, 1
    for ray in range(num_of_rays):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        x, dx = (xm + 100, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WORLD_WIDTH, 100):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * 100
        y, dy = (ym + 100, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, WORLD_HEIGHT, 100):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * 100
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % 100
        depth *= math.cos(player_angle - cur_angle)
        depth = max(depth, 0.00001)
        proj_height = int(projection_coeff / depth)

        casted_walls.append((depth, offset, proj_height, texture))
        cur_angle += delta
    return casted_walls


def raycasting_walls(player, textures):
    walls = []
    casted_walls = raycasting(player.pos, player.angle, world_map)
    wall_shot = casted_walls[num_of_rays // 2 - 1][0], casted_walls[num_of_rays // 2 - 1][2]

    for ray, casted_values in enumerate(casted_walls):
        depth, offset, proj_height, texture = casted_values

        if proj_height > HEIGHT:
            texture_height = TEXTURE_HEIGHT / (proj_height / HEIGHT)
            wall_column = textures[texture].subsurface(offset * (TEXTURE_WIDTH // 100),
                                                       TEXTURE_HEIGHT // 2 - texture_height // 2,
                                                       TEXTURE_WIDTH // 100, texture_height)
            wall_column = pygame.transform.scale(wall_column, (scaling, HEIGHT))

            wall_pos = (ray * scaling, 0)
        else:
            wall_column = textures[texture].subsurface(offset * (TEXTURE_WIDTH // 100),
                                                       0, (TEXTURE_WIDTH // 100), TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(wall_column, (scaling, proj_height))
            wall_pos = (ray * scaling, HEIGHT // 2 - proj_height // 2)

        walls.append((depth, wall_column, wall_pos))

    return walls, wall_shot
