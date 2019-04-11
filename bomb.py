from bullet import Bullet
import pygame

class Bomb(Bullet):
    def __init__(self, image, screen, shooter_rect, speed, animation_frames, rotation=0):
        super().__init__(image, screen, shooter_rect, speed, rotation)
        self.anim_frames = animation_frames
        self.frame_index = 0
        self.frame_shown = pygame.time.get_ticks()

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.frame_shown > 150:
            self.frame_shown = now
            if self.frame_index < len(self.anim_frames) - 1:
                self.frame_index += 1
            else:
                self.frame_index = 0
            self.image = self.anim_frames[self.frame_index]

    def update(self):
        super().update()
        self.animate()

