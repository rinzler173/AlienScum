from player import Player
from pygame import Vector2 as Vec
import random


class AutoPlayer(Player):
    """autonomous, computer-controlled player entity"""
    def __init__(self, screen, all_sprites, target_sprites, bullet_sprites):
        super().__init__(screen, all_sprites)
        self.bullets = bullet_sprites
        self.targets = target_sprites
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.height*3/4
        self.pos = self.rect.center
        self.original_pos = self.pos
        self.correcting_x = False
        self.correcting_y = False
        self.max_drift = [0, 0]

    def update(self):
        if not self.departing:
            self.move_around()
            self.manage_pilotage()
            self.pos += self.velocity
            self.rect.center = self.pos
        else:
            super().update()

    def manage_pilotage(self):
        if len(self.bullets) == 0:
            #  any target
            for target in self.targets:
                #  at least as close as 2/3 of the screen on y axis
                if target.rect.left <= self.rect.centerx <= target.rect.right:
                    #  and in canon range
                    if self.rect.y - target.rect.y <= self.screen_rect.height*2/3:
                        #  will be shot
                        self.shoot().add(self.bullets, self.all_sprites)

    def move_around(self):
        # x axis
        if self.velocity.x == 0:
            self.velocity[0] = random.choice((-1, 1))
            self.max_drift[0] = random.randint(35, 50) * self.velocity[0]

        if self.original_pos[0] + self.max_drift[0] == self.pos[0]:
            self.velocity[0] *= -1
            self.correcting_x = True
        if self.correcting_x and self.pos[0] == self.original_pos[0]:
            self.correcting_x = False
            self.velocity.x = 0

        # y axis
        if self.velocity.y == 0:
            self.velocity[0] = random.choice((-1, 1))
            self.max_drift[0] = random.randint(35, 50) * self.velocity[0]

        if self.original_pos[0] + self.max_drift[0] == self.pos[0]:
            self.velocity[0] *= -1
            self.correcting_x = True
        if self.correcting_x and self.pos[0] == self.original_pos[0]:
            self.correcting_x = False
            self.velocity.x = 0












