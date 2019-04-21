from pygame.sprite import Sprite


class Animation(Sprite):
    def __init__(self, screen, frames, x_spawn, y_spawn, frames_for_image=3, repeat=0):
        super(Animation, self).__init__()
        self.frames_for_image = frames_for_image
        self.screen = screen
        self.frame_index = 0
        self.repeat = repeat  # use negative number for infinite loop
        self.animation = frames
        self.animation_frames = len(frames)
        self.image = frames[0]
        self.rect = self.image.get_rect()
        self.x_spawn = x_spawn
        self.y_spawn = y_spawn
        self.rect.centerx = x_spawn
        self.rect.centery = y_spawn
        self.frames_lifespan = 0  # how many game fps/update calls passed since frame was changed

    def update(self):
        if self.frames_lifespan % self.frames_for_image == 0:
            self.image = self.animation[self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.centerx = self.x_spawn
            self.rect.centery = self.y_spawn
            if self.frame_index+1 >= self.animation_frames:
                if self.repeat == 0:
                    self.kill()
                else:
                    self.frame_index = 0
                    self.repeat -= 1
            else:
                self.frame_index += 1
        self.frames_lifespan += 1

    def blitime(self):
        self.screen.blit(self.image, self.rect)
