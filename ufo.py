from enemy import Enemy
from guided_bullet import GuidedBullet
from settings import UfoConfig as config

class Ufo(Enemy):
    def __init__(self, screen, spawn_x, spawn_y, all_sprites, bullet_sprites, player):
        super().__init__(screen, spawn_x, spawn_y, config, all_sprites, bullet_sprites)
        self.player = player

    def getShot(self):
        shot = []
        shot.append(GuidedBullet(self.bullet_image, self.screen, self.rect, self.config.bullet_speed, self.player))
        return shot



