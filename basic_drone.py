from enemy import Enemy
from settings import BasicDroneConfig as config


class BasicDrone(Enemy):
    def __init__(self, screen, spawn_x, spawn_y, all_sprites, bullet_sprites):
        super().__init__(screen, spawn_x, spawn_y, config, all_sprites, bullet_sprites)



