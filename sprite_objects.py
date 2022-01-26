import pygame
from settings import *

double_width = 2 * WIDTH
double_height = 2 * HEIGHT
fakerays_range = 300 - 1 + 2 * 200
scaling = WIDTH // 300
fov = math.pi / 3
projection_coeff = 3 * (300 / (2 * math.tan(fov / 2))) * 100
delta = fov / 300


class Sprites:
    def __init__(self):
        self.sprites_params = {
            'sprite_stand': {
                'sprite': pygame.image.load('sprites/standing_target/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.8,
                'scale': (0.4, 0.4),
                'side': 30,
                'blocking': True,
                'flag': '',
            },
            'npc_target': {
                'sprite': pygame.image.load(f'sprites/npc/target/base/0.png').convert_alpha(),
                'viewing_angles': True,
                'shift': 0.8,
                'scale': (0.4, 0.6),
                'side': 30,
                'blocking': True,
                'flag': 'npc',
            }
        }
        self.object_list = [
            SpriteObject(self.sprites_params['sprite_stand'], (7.1, 2.1)),
            SpriteObject(self.sprites_params['sprite_stand'], (5.9, 2.1)),
            SpriteObject(self.sprites_params['sprite_stand'], (14.8, 12.28)),
            SpriteObject(self.sprites_params['sprite_stand'], (16.5, 7.61)),
            SpriteObject(self.sprites_params['sprite_stand'], (12.54, 2.42)),
            SpriteObject(self.sprites_params['sprite_stand'], (19.2, 2.62)),
            SpriteObject(self.sprites_params['sprite_stand'], (21.79, 8.93)),
            SpriteObject(self.sprites_params['sprite_stand'], (21.57, 13.58)),
            SpriteObject(self.sprites_params['sprite_stand'], (12.32, 13.62)),

            SpriteObject(self.sprites_params['npc_target'], (2.5, 1)),
            SpriteObject(self.sprites_params['npc_target'], (21.5, 1)),
        ]

    @property
    def sprite_shot(self):
        return min([obj.target_shot for obj in self.object_list], default=(float('inf'), 0))


class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.blocking = parameters['blocking']
        self.flag = parameters['flag']
        self.x, self.y = pos[0] * 100, pos[1] * 100
        self.side = parameters['side']
        self.dead_animation_count = 0
        self.npc_action_trigger = False
        self.delete = False


    @property
    def target_shot(self):
        if (300 // 2 - 1) - self.side // 2 < self.current_ray \
                < (300 // 2 - 1) + self.side // 2 and self.blocking:
            return (self.distance_to_sprite, self.proj_height)

        return (float('inf'), None)

    @property
    def sprite_position(self):
        return self.x - self.side // 2, self.y - self.side // 2

    def object_locate(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)
        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle

        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += math.pi * 2

        self.theta -= 1.4 * gamma
        delta_rays = int(gamma / delta)
        self.current_ray = (300 // 2 - 1) + delta_rays
        self.distance_to_sprite *= math.cos((fov / 2) - self.current_ray * delta)
        fake_ray = self.current_ray + 200

        if 0 <= fake_ray <= fakerays_range and self.distance_to_sprite > 30:
            self.proj_height = min(int(projection_coeff / self.distance_to_sprite),
                                   double_height)
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift
            self.object = self.visible_sprite()
            sprite = pygame.transform.scale(self.object, (sprite_width, sprite_height))
            sprite_pos = (self.current_ray * scaling - half_sprite_width,
                          HEIGHT // 2 - half_sprite_height + shift)
            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    def visible_sprite(self):
        return self.object
