from raycast import mapping
import math
import pygame
from numba import njit

tile = 100


@njit(fastmath=True, cache=True)
def ray_casting_npc_player(npc_pos_x, npc_pos_y, player_pos):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_pos_x, oy - npc_pos_y
    angle = math.atan2(delta_y, delta_x)
    angle += math.pi

    sin_a = math.sin(angle)
    cos_a = math.cos(angle)

    x, dx = (xm + tile, 1) if cos_a >= 0 else (xm, -1)
    for i in range(int(abs(delta_x) // tile)):
        x += dx * tile

    y, dy = (ym + tile, 1) if sin_a >= 0 else (ym, -1)
    for i in range(int(abs(delta_y) // tile)):
        y += dy * tile
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        self.shot_sound = pygame.mixer.Sound('sound/shot.mp3')
        self.reverse = False
        self.score = 0

    def object_interaction(self):
        if self.player.shot and self.drawing.shot_animation_trigger:
            for obj in sorted(self.sprites.object_list, key=lambda obj: obj.distance_to_sprite):
                if obj.target_shot[1]:
                    self.shot_sound.play()
                    self.score += 10
                    break

        return self.score

    def npc_action(self):
        for object in self.sprites.object_list:
            if object.flag == 'npc':
                if ray_casting_npc_player(object.x, object.y, self.player.pos):
                    self.npc_move(object)

    def npc_move(self, object):
        if not self.reverse:
            object.x = object.x
            object.y = object.y + 1

            if object.y >= 1500:
                self.reverse = True

        if self.reverse:
            object.x = object.x
            object.y = object.y - 1

            if object.y <= 1:
                self.reverse = False
