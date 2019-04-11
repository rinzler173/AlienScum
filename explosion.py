from pygame.sprite import Sprite


class Explosion(Sprite):
    def __init__(self, screen, animation, x_spawn, y_spawn):
        super(Explosion, self).__init__()
        self.screen = screen
        self.frame_index = 0
        self.animation = animation
        self.animation_frames = len(animation)
        self.image = animation[0]
        self.rect = self.image.get_rect()
        self.x_spawn = x_spawn
        self.y_spawn = y_spawn
        self.rect.centerx = x_spawn
        self.rect.centery = y_spawn
        self.frames_lifespan = 0  # how many game fps/update calls passed since frame was changed

    def update(self):
        if self.frames_lifespan % 3 == 0:
            self.image = self.animation[self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.centerx = self.x_spawn
            self.rect.centery = self.y_spawn
            if self.frame_index+1 >= self.animation_frames:
                self.kill()
            else:
                self.frame_index += 1
        self.frames_lifespan += 1

    def blitime(self):
        self.screen.blit(self.image, self.rect)
