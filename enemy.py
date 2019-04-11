from mob import Mob
import pygame
import random
import math
from bullet import Bullet


class Enemy(Mob):
    def __init__(self, screen, spawn_x, spawn_y, config, all_sprites, bullet_sprites):
        super().__init__(screen, config, spawn_x, spawn_y, all_sprites)
        self.all_sprites = all_sprites
        self.bullet_sprites = bullet_sprites

        self.last_update = pygame.time.get_ticks()
        self.moving = True

        self.odds = []
        for i in range(math.ceil((1-self.config.skipped_shots)*100)):
            self.odds.append(True)
        for i in range(math.ceil(self.config.skipped_shots*100)):
            self.odds.append(False)

    def getShot(self):
        shot = []
        bullet = Bullet(self.bullet_image, self.screen, self.rect, self.config.bullet_speed, rotation=180)
        shot.append(bullet)
        return shot

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000/self.config.fire_rate:
            self.last_update = now
            fired = random.choice(self.odds)
            if fired:
                shot = self.getShot()
                for bullet in shot:
                    self.all_sprites.add(bullet)
                    self.bullet_sprites.add(bullet)
                    random.choice(self.shoot_sounds).play()

    def update(self):
        self.shoot()
        if self.moving:
            if 0 < self.rect.left < self.screen_rect.width:
                self.rect.x += self.config.speed




