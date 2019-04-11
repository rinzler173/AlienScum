from enemy import Enemy
from settings import TrishotDroneConfig as config
from bullet import Bullet


class TrishotDrone(Enemy):
    def __init__(self, screen, spawn_x, spawn_y, all_sprites, bullet_sprites):
        super().__init__(screen, spawn_x, spawn_y, config, all_sprites, bullet_sprites)

    def getShot(self):
        shot = super().getShot()
        shot.append(Bullet(self.bullet_image, self.screen, self.rect, self.config.bullet_speed, rotation=160))
        shot.append(Bullet(self.bullet_image, self.screen, self.rect, self.config.bullet_speed, rotation=200))
        return shot
