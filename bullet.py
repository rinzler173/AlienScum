from pygame.sprite import Sprite
import pygame as pg
vec = pg.math.Vector2

class Bullet(Sprite):
    """defines basic bullet entity shot by player or enemy"""
    def __init__(self, image, screen, shooter_rect, speed, rotation=0):
        super(Bullet, self).__init__()
        self.rotation = rotation
        self.image = image
        self.image_copy = self.image.copy()
        self.rect = self.image.get_rect()
        self.screen = screen
        self.speed = speed
        self.vel_vec = vec(0, 0)
        # make bullet spawn inside center top of the ship (to look like it's coming out of it's canon)
        self.rect.centerx = shooter_rect.centerx
        self.rect.center = shooter_rect.center

        self.rotate(0)

    def rotate(self, degrees):
        self.rotation += degrees
        self.rotation = self.rotation % 360
        new_image = pg.transform.rotate(self.image_copy, self.rotation)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        if 0 <= self.rotation < 90:
            self.vel_vec.y = -abs(self.speed)
            self.vel_vec.x = self.vel_vec.y * self.rotation / 90
            self.vel_vec.y -= self.vel_vec.x

        if 90 <= self.rotation < 180:
            self.vel_vec.y = abs(self.speed)
            self.vel_vec.x = -(self.vel_vec.y * (1-(self.rotation - 90) / 90))
            self.vel_vec.y += self.vel_vec.x

        if 180 <= self.rotation < 270:
            self.vel_vec.y = abs(self.speed)
            self.vel_vec.x = self.vel_vec.y * (self.rotation - 180) / 90
            self.vel_vec.y -= self.vel_vec.x

        if 270 <= self.rotation < 360:
            self.vel_vec.y = -abs(self.speed)
            self.vel_vec.x = -self.vel_vec.y * (1-(self.rotation - 270) / 90)
            self.vel_vec.y += self.vel_vec.x


    def update(self):
        self.rect.center += self.vel_vec

    def blitime(self):
        self.screen.blit(self.image, self.rect)
