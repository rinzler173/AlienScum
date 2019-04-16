from enemy import Enemy
from bomb import Bomb
from utils import *
from settings import BomberDroneConfig as config


class BomberDrone(Enemy):
    def __init__(self, screen, spawn_x, spawn_y, all_sprites, bullet_sprites, friendlies_sprites):
        super().__init__(screen, spawn_x, spawn_y, config, all_sprites, bullet_sprites, friendlies_sprites)
        self.bullet_anim = []
        for frame_name in self.config.bullet_frames:
            self.bullet_anim.append(load_image(frame_name))

    def getShot(self):
        shot = []
        shot.append(Bomb(self.bullet_image, self.screen, self.rect, self.config.bullet_speed, self.bullet_anim, rotation = 180))
        return shot