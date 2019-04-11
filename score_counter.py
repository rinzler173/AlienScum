from pygame.sprite import Sprite
from pygame.font import Font


class ScoreCounter(Sprite):
    def __init__(self, player, screen, font_name, size, color):
        super(ScoreCounter, self).__init__()
        self.screen = screen
        self.score = 0
        self.color = color
        self.font = Font(font_name, size)
        self.image = self.font.render(str(self.score), True, self.color)
        self.rect = self.image.get_rect()
        self.player = player
        self.increased = False

    def update(self):
        if self.increased:
            self.image = self.font.render(str(self.score), True, self.color)
            self.rect = self.image.get_rect()
            self.increased = False
        self.rect.midtop = (self.player.rect.centerx, self.player.rect.centery + 7)

    def blitime(self):
        self.screen.blit(self.image, self.rect)

    def score_kill(self, victim):
        self.score += victim.config.value
        self.increased = True


