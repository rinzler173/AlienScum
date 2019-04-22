from mob import Mob
from bullet import Bullet
from settings import Config
from jet_animation import JetAnimation
import random
from pygame.math import Vector2 as Vec


class Player(Mob):
    """Basic class representing players entity in the game"""
    def __init__(self, screen, all_sprites, departing=False):
        super().__init__(screen, Config, 0, 0, all_sprites)
        self.screen = screen
        self.speed = Config.speed
        self.departing = departing

        # start each new player at the bottom of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - Config.bottom_margin - Config.vertical_leeway
        self.velocity = Vec(0, 0)
        self.acceleration = Vec(0, 0)
        self.pos = Vec(self.rect.center)

        self.mov_flags = {'left': False, 'right': False, 'down': False, 'up': False}

    # update visible properties
    def update(self):
        if not self.departing:
            if self.mov_flags['left'] and (self.rect.left > Config.horizontal_margin):
                self.acceleration.x = -1.0
            elif self.mov_flags['right'] and (self.rect.right <= (self.screen_rect.width - Config.horizontal_margin)):
                self.acceleration.x = 1.0
            elif self.mov_flags['down'] and (self.rect.bottom <= (self.screen_rect.height - Config.bottom_margin)):
                pass
            elif self.mov_flags['up'] and (self.rect.top > (self.screen_rect.height -
                                        (Config.bottom_margin + self.rect.height + Config.vertical_leeway * 2))):
                pass
            else:
                self.acceleration = Vec(0, 0)

        self.acceleration.x += self.velocity.x * -0.05
        self.pos += self.velocity + self.acceleration/2
        self.velocity += self.acceleration
        self.rect.center = self.pos
    # returns bullet entity that can be added to sprites group
    def shoot(self):
        bullet = Bullet(self.bullet_image, self.screen, self.rect, Config.bullet_speed)
        random.choice(self.shoot_sounds).play()
        return bullet

    #  after completing a level
    def fly_away(self):
        self.departing = True
        self.velocity.x = 0
        self.acceleration.x = 0
        self.acceleration.y = -0.04
        self.all_sprites.add(JetAnimation(self.screen, self.config.jet_anim_dir, self))








