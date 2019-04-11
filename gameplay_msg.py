from pygame.sprite import Sprite
from pygame.font import Font

class GameplayMsg(Sprite):
    MSG_FADE = 1
    MSG_PULSE = 2

    def __init__(self, screen, font_name, init_size, peak_size, interval, color, text, kind):
        super(GameplayMsg, self).__init__()
        self.type = kind
        self.screen = screen
        self.text = text
        self.color = color
        self.font_name = font_name
        self.font = Font(font_name, init_size)
        self.init_size = init_size
        self.current_size = init_size
        self.peak_size = peak_size
        self.interval = interval
        self.image = self.font.render(str(self.text), True, self.color)
        self.rect = self.image.get_rect()
        self.growing = True


    def update(self):
        self.font = Font(self.font_name, self.current_size)
        self.image = self.font.render(str(self.text), True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)

        if self.current_size < self.peak_size and self.growing:
            self.current_size += self.interval
        elif self.type == GameplayMsg.MSG_FADE:
            self.growing = False
            if self.current_size <= 0:
                self.kill()
            else:
                self.current_size -= self.interval
        elif self.type == GameplayMsg.MSG_PULSE:
            self.growing = False
            if self.current_size <= self.init_size:
                self.growing = True
            else:
                self.current_size -= self.interval

    def blitime(self):
        self.screen.blit(self.image, self.rect)


