from pygame.sprite import Sprite
from pygame.math import Vector2 as Vec
from utils import *
from settings import Game as config

class Debries(Sprite):
    """Abstract class for all kinds of debries and fragments rotating and flying along the screen"""
    def __init__(self, screen, image, spawn_x, spawn_y):
        super(Debries, self).__init__()

        self.screen = screen
        self.config = config
        self.image_orig = image
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = spawn_x
        self.rect.centery = spawn_y
        self.velocityVec = Vec(random.randrange(config.min_expl_vel, config.max_expl_vel),
                            random.randrange(config.min_expl_vel, config.max_expl_vel))
        self.rot_speed = random.randrange(config.min_expl_rot, config.max_expl_rot)
        self.last_rotate = pygame.time.get_ticks()
        self.rot = 0

    def update(self):
        self.rect.center += self.velocityVec
        self.rotate()

    def blitime(self):
        self.screen(self.image, self.rect)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_rotate > 50:
            self.last_rotate = now
        self.rot = (self.rot + self.rot_speed) % 360
        new_image = pygame.transform.rotate(self.image_orig, self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center








