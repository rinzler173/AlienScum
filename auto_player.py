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
        self.original_pos = Vec(self.rect.center)
        self.moving_x = False
        self.moving_y = False
        self.correcting_x = False
        self.correcting_y = False
        self.current_x_drift = 0
        self.max_x_drift = 0
        self.x_drift_vel = 0
        self.current_y_drift = 0
        self.max_y_drift = 0
        self.y_drift_vel = 0


    def update(self):
        self.manage_pilotage()
        self.move_around()

    def manage_pilotage(self):
        if not self.departing and len(self.bullets) == 0:
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
        if not self.moving_x:
            self.x_drift_vel = random.choice((-1, 1))
            self.max_x_drift = random.randint(30, 60)
            self.current_x_drift = 0
            self.moving_x = True

        if self.current_x_drift < self.max_x_drift and not self.correcting_x:
            self.current_x_drift += 1
            self.rect.centerx += self.x_drift_vel
        elif not self.correcting_x:
            self.x_drift_vel = -self.x_drift_vel
            self.correcting_x = True
        elif self.correcting_x and self.current_x_drift > 0:
            self.current_x_drift -= 1
            self.rect.centerx += self.x_drift_vel
        else:
            self.correcting_x = False
            self.moving_x = False

        # y axis
        if not self.moving_y:
            self.y_drift_vel = random.choice((-1, 1))
            self.max_y_drift = random.randint(20, 40)
            self.current_y_drift = 0
            self.moving_y = True

        if self.current_y_drift < self.max_y_drift and not self.correcting_y:
            self.current_y_drift += 1
            self.rect.centery += self.y_drift_vel
        elif not self.correcting_y:
            self.y_drift_vel = -self.y_drift_vel
            self.correcting_y = True
        elif self.correcting_y and self.current_y_drift > 0:
            self.current_y_drift -= 1
            self.rect.centery += self.y_drift_vel
        else:
            self.correcting_y = False
            self.moving_y = False












