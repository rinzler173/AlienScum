from mob import Mob
from bullet import Bullet
from settings import Config
import random


class Player(Mob):
    """Basic class representing players entity in the game"""
    def __init__(self, screen, all_sprites):
        super().__init__(screen, Config, 0, 0, all_sprites)
        self.screen = screen
        self.speed = Config.speed

        # start each new player at the bottom of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - Config.bottom_margin - Config.vertical_leeway

        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        self.mov_flags = {'left': False, 'right': False, 'down': False, 'up': False}

    # update visible properties
    def update(self):
        if self.mov_flags['left'] and (self.rect.left > Config.horizontal_margin):
            self.centerx -= Config.speed
        if self.mov_flags['right'] and (self.rect.right <= (self.screen_rect.width - Config.horizontal_margin)):
            self.centerx += Config.speed
        if self.mov_flags['down'] and (self.rect.bottom <= (self.screen_rect.height - Config.bottom_margin)):
            self.centery += Config.speed
        if self.mov_flags['up'] and (self.rect.top > (self.screen_rect.height -
                                                      (Config.bottom_margin + self.rect.height + Config.vertical_leeway * 2))):
            self.centery -= self.speed

        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    # returns bullet entity that can be added to sprites group
    def shoot(self):
        bullet = Bullet(self.bullet_image, self.screen, self.rect, Config.bullet_speed)
        random.choice(self.shoot_sounds).play()
        return bullet


