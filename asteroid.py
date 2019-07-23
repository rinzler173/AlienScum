from mob import Mob
import os
import random
import utils
from pygame.math import Vector2 as Vec
from animation import Animation
from settings import AsteroidConfig as Config



class Asteroid(Mob):
    def __init__(self, screen, all_sprites, rotation=0, speed=None):
        super().__init__(screen, Config, 0, 0, all_sprites)
        self.size = "medium"
        self.image = self.get_random_asteroid()
        self.rect = self.image.get_rect()
        self.rect.bottom = self.screen_rect.top
        self.rect.centerx = random.choice(range(0, self.screen_rect.right))
        self.pos = Vec(self.rect.center)
        if rotation == 0:
            rotation_reaches = eval("Config."+self.size+"_rot_reach")
            self.rotation = random.choice(range(rotation_reaches)) * random.choice([-1, 1])
        else:
            self.rotation = rotation

        if not speed:
            x_speed_reaches = eval("Config.common_horizontal_speed_reach")
            x_speed = random.choice(range(x_speed_reaches[0], x_speed_reaches[1]))
            # will drift right if occupies left side of the screen, otherwise left
            if self.rect.centerx > self.screen_rect.centerx:
                x_speed *= -1
            y_speed_reaches = eval("Config."+self.size+"_vertical_speed_reach")
            y_speed = random.choice(range(y_speed_reaches[0], y_speed_reaches[1]))
            self.speed = Vec(x_speed, y_speed)
        else:
            self.speed = speed

    def update(self):
        self.pos += self.speed
        self.rect.center = self.pos

    # handles sound effect and animation, deletes sprite
    def onDestroy(self):
        if self.size == "big":
            self.death_sounds[1].play()
        else:
            self.death_sounds[0].play()
        self.all_sprites.add(Animation(self.screen, self.config.explosion_anim_dir,
                                       self.rect.centerx, self.rect.centery))
        if self.alive():
            self.kill()

    # returns random asteroid of random size
    def get_random_asteroid(self):
        self.size = random.choice(["tiny", "small", "medium", "big"])
        image = utils.load_image(rel_path=os.path.join("images", "mobs", "asteroids", self.size))
        return image
