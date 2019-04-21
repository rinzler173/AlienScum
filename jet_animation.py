from animation import Animation


class JetAnimation(Animation):
    def __init__(self, screen, frames, ship, frames_for_image=3, repeat=0):
        super().__init__(screen, frames, 0, 0, frames_for_image, repeat)
        self.ship_rect = ship.rect

    def update(self):
        self.rect.midtop = self.ship_rect.midbottom
        if self.frames_lifespan % self.frames_for_image == 0:
            self.image = self.animation[self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.midtop = self.ship_rect.midbottom
            if self.frame_index+1 >= self.animation_frames:
                if self.repeat == 0:
                    self.kill()
                else:
                    self.frame_index = 0
                    self.repeat -= 1
            else:
                self.frame_index += 1
        self.frames_lifespan += 1


