from animation import Animation
import pygame


class JetAnimation(Animation):
    def __init__(self, screen, anim_dir, ship, frames_for_image=30, repeat=0, flicker=6):
        super().__init__(screen, anim_dir, 0, 0, frames_for_image, repeat)
        self.ship = ship
        self.flicker = flicker
        self.faded_frame = pygame.Surface((0, 0))  # empty frame for blinking effect
        self.faded = False

    def update(self):
        if self.ship.alive():
            if self.faded:
                self.image = self.frames[self.frame_index]
            self.rect.midtop = self.ship.rect.midbottom
            if self.frames_lifespan % self.frames_for_image == 0:
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect()
                self.rect.midtop = self.ship.rect.midbottom
                if self.frame_index+1 < self.animation_frames:
                    self.frame_index += 1
                else:
                    self.flicker = 15
            elif self.flicker > 0 and self.frames_lifespan != 0 and self.frames_lifespan % self.flicker == 0:
                self.image = self.faded_frame
                self.faded = True
            self.frames_lifespan += 1
        else:
            self.kill()


