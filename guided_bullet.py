import pygame as pg
vec = pg.math.Vector2
from pygame.sprite import Sprite

import pygame
import math

class GuidedBullet(Sprite):
    def __init__(self, image, screen, shooter_rect, speed, target):
        super(GuidedBullet, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.screen = screen
        self.shooter_rect = shooter_rect
        self.rect.center = shooter_rect.center
        self.speed = speed
        self.vel_vec = vec(0, self.speed)
        self.target = target
        self.last_update = pygame.time.get_ticks()
        self.targetx = self.target.rect.centerx
        self.deviation = self.targetx - self.rect.centerx
        self.frames_to_target = math.ceil((self.target.rect.top - self.rect.bottom) / self.vel_vec.y)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 333:
            self.last_update = now
            self.targetx = self.target.rect.centerx
            self.deviation = self.targetx - self.rect.centerx
            self.frames_to_target = math.ceil((self.target.rect.top - self.rect.bottom) / self.vel_vec.y)
        if self.frames_to_target > 0:
            correction = self.deviation / self.frames_to_target  # per frame
            if correction > 5 and self.frames_to_target < 15:
                correction = 5
            if correction < -5 and self.frames_to_target < 15:
                correction = -5
            # keep moving down while gradually aligning x-axis to target
            self.rect.x += correction
        self.rect.y += self.vel_vec.y



