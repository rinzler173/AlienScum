import pygame
import shelve
import utils
import random
from settings import Game as GameConfig
from settings import Config as PlayerConfig
from auto_player import AutoPlayer
from asteroid import Asteroid
from jet_animation import JetAnimation


class MainMenu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.save = shelve.open('game_save')
        self.screen = pygame.display.set_mode(GameConfig.screen_res)
        self.caption = pygame.display.set_caption(GameConfig.caption)
        self.background_img = utils.load_image(GameConfig.background_img_file)
        self.background_rect = self.background_img.get_rect()
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.asteroid_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.player = AutoPlayer(self.screen, self.all_sprites, self.asteroid_sprites, self.bullet_sprites)
        self.player.add(self.all_sprites, self.player_sprites)
        self.all_sprites.add(JetAnimation(self.screen, PlayerConfig.jet_anim_dir, self.player))

    def run_menu(self):
        while self.running:
            self.clock.tick(GameConfig.FPS)
            self.all_sprites.update()
            self.manage_asteroids()
            self.throw_asteroids()
            # render graphics
            self.screen.blit(self.background_img, self.background_rect)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

    def throw_asteroids(self):
        can_add = GameConfig.max_asteroids_on_screen - len(self.asteroid_sprites)
        asteroids_to_throw = random.randint(0, can_add)

        for i in range(asteroids_to_throw):
            Asteroid(self.screen, self.all_sprites).add(self.all_sprites, self.asteroid_sprites)

    def manage_asteroids(self):
        for asteroid in self.asteroid_sprites:
            if asteroid.rect.y > asteroid.screen_rect.bottom:
                asteroid.kill()
        hits = pygame.sprite.groupcollide(self.asteroid_sprites, self.bullet_sprites, True, True)
        for hit in hits:
            hit.onDestroy()
