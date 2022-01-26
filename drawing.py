import pygame
from settings import *
from collections import deque


class Drawing:
    def __init__(self, sc, player, clock):
        self.sc = sc
        self.player = player
        self.clock = clock
        self.font = pygame.font.SysFont('Arial', 36)
        self.textures = {1: pygame.image.load('img/1.jpg').convert()}
        self.weapon_base_sprite = pygame.image.load('sprites/weapons/shotgun/base/0.png').convert_alpha()
        self.weapon_shot_animation = deque([pygame.image.load(f'sprites/weapons/shotgun/shot/{i}.png')
                                           .convert_alpha() for i in range(3)])
        self.weapon_rect = self.weapon_base_sprite.get_rect()
        self.weapon_pos = (WIDTH // 2 - self.weapon_rect.width // 2, HEIGHT - self.weapon_rect.height)
        self.shot_length = len(self.weapon_shot_animation)
        self.shot_length_count = 0
        self.shot_animation_trigger = True
        self.shot_animation_speed = 3
        self.shot_animation_count = 0
        self.shot_sound = pygame.mixer.Sound('sound/shotgun.mp3')
        self.sfx = deque([pygame.image.load(f'sprites/weapons/sfx/{i}.png').convert_alpha() for i in range(8)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)

    def background(self):
        self.sc.fill((0, 0, 0))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, object_pos)

    def player_weapon(self, shot_projections):
        if self.player.shot:
            if not self.shot_length_count:
                self.shot_sound.play()
            self.shot_projection = min(shot_projections)[1] // 2
            self.bullet_sfx()
            shot_sprite = self.weapon_shot_animation[0]
            self.sc.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count += 1
            if self.shot_animation_count == self.shot_animation_speed:
                self.weapon_shot_animation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_length_count += 1
                self.shot_animation_trigger = False
            if self.shot_length_count == self.shot_length:
                self.player.shot = False
                self.shot_length_count = 0
                self.sfx_length_count = 0
                self.shot_animation_trigger = True
        else:
            self.sc.blit(self.weapon_base_sprite, self.weapon_pos)

    def bullet_sfx(self):
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.sc.blit(sfx, (WIDTH // 2 - sfx_rect.width // 2, HEIGHT // 2 - sfx_rect.height // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, (220, 0, 0))
        self.sc.blit(render, FPS_POS)

    def score(self, score):
        display_score = str(score)
        render = self.font.render(display_score, 0, (220, 0, 0))
        self.sc.blit(render, SCORE_POS)
