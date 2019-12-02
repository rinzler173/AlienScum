import pygame
import shelve
import sys
import utils
import os
import xml.etree.ElementTree as et
from utils import Colors as RGB
from settings import Game
from player import Player
from basic_drone import BasicDrone
from score_counter import ScoreCounter
from ufo import Ufo
from trishot_drone import TrishotDrone
from bomber_drone import BomberDrone
from gameplay_msg import GameplayMsg as Msg


class Gameplay:
    def __init__(self):
        # initialize pygame, setup screen
        pygame.init()
        pygame.mixer.init()
        self.save = shelve.open('game_save')
        self.running = True
        self.can_restart = False
        self.manage_death = False
        self.manage_victory = False
        self.god_mode = Game.god_mode
        self.current_level = self.save['current_level']
        self.sounds = {}
        self.msg = {}
        self.sounds['level_completed'] = utils.load_sound('level_completed.wav')
        self.sounds['game_completed'] = utils.load_sound('game_completed.wav')
        self.screen = pygame.display.set_mode(Game.screen_res)
        pygame.display.set_caption(Game.caption)
        self.interface_font = pygame.font.match_font(Game.interface_font_name)
        self.background_img = utils.load_image(Game.background_img_file)
        self.background_rect = self.background_img.get_rect()
        self.clock = pygame.time.Clock()

        # initialize sprites
        self.all_sprites = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.player = Player(self.screen, self.all_sprites)
        self.player.add(self.all_sprites, self.player_sprites)
        self.player_score = ScoreCounter(self.player, self.save['player_score'], self.screen, self.interface_font, 25, RGB.BLACK)
        self.msg['game_completed'] = Msg(self.screen, self.interface_font, 65, 90, 1, RGB.GREEN,
                                         "Congratulations! Game completed!", Msg.MSG_PULSE)
        self.msg['lvl_completed'] = Msg(self.screen, self.interface_font, 100, 175, 2, RGB.GREEN, "Victory!", Msg.MSG_PULSE)
        self.msg['player_killed'] = Msg(self.screen, self.interface_font, 100, 175, 2, RGB.RED, "Game Over!", Msg.MSG_FADE)
        self.endgame_initiated = None
        self.player_score.add(self.all_sprites)
        self.player_bullets = pygame.sprite.Group()

        self.enemy_rows = []
        self.read_xml()

    def run_gameplay(self):
        # Game loop
        while self.running:
            # handle events
            self.clock.tick(Game.FPS)
            self.check_events()
            self.manage_restart()
            # update sprites
            self.delete_invisible()
            self.all_sprites.update()
            self.check_collisions()
            # render graphics
            self.screen.blit(self.background_img, self.background_rect)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
        self.on_gameplay_stop()

    # save persistent data
    def on_gameplay_stop(self):
        self.save['current_level'] = self.current_level
        self.save['player_score'] = self.player_score.score

    def reset_progress(self):
        self.current_level = 1
        self.player_score.score = 0

    # all game loop inner functions below
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.on_keydown(event)
            elif event.type == pygame.KEYUP:
                self.on_keyup(event)
            elif event.type == pygame.QUIT:
                sys.exit()

    # manages key presses
    def on_keydown(self, event):
        if self.player.alive():
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.player.mov_flags['left'] = True
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.player.mov_flags['right'] = True
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.player.mov_flags['down'] = True
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.player.mov_flags['up'] = True
            elif event.key == pygame.K_SPACE:
                bullet = self.player.shoot()
                self.all_sprites.add(bullet)
                self.player_bullets.add(bullet)
        elif event.key == pygame.K_r and self.can_restart:
            self.running = False

    # manages key releases
    def on_keyup(self, event):
        if self.player.alive():
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.player.mov_flags['left'] = False
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.player.mov_flags['right'] = False
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.player.mov_flags['down'] = False
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.player.mov_flags['up'] = False

    # creates as many enemies of given class as can fit a single row
    # returns list representing the row
    # rows above argument should be combined height of all rows above (without margins)
    def get_uniform_row(self, enemy_class, rows_above):
        enemy = enemy_class(self.screen, 0, 0, self.all_sprites, self.enemy_bullets, self.enemy_sprites)
        y_margin = self.screen.get_rect().height * .09
        fittable_enemies = int(self.screen.get_rect().width / (enemy.rect.width * 2))
        uniform_row = []
        for index in range(fittable_enemies):
            uniform_row.append(enemy_class(self.screen, enemy.rect.width + (enemy.rect.width * 2 * index), y_margin + rows_above * y_margin * 2,
                                           self.all_sprites, self.enemy_bullets, self.enemy_sprites))
        return uniform_row

    def get_mixed_row(self, enemy_classes, rows_above):
        mixed_row = []
        y_margin = self.screen.get_rect().height * .09
        x_margin = 0
        screen_width = self.screen.get_rect().width
        enemies_width = 0
        for enemy_class in enemy_classes:
            if enemy_class == Ufo:
                enemy = enemy_class(self.screen, 0, 0, self.all_sprites, self.enemy_bullets, self.player, self.enemy_sprites)
            else:
                enemy = enemy_class(self.screen, 0, 0, self.all_sprites, self.enemy_bullets, self.enemy_sprites)
            if (enemies_width + enemy.rect.width + enemies_width + enemy.rect.width / (len(mixed_row) + 1)) <= screen_width:
                enemies_width += enemy.rect.width
                mixed_row.append(enemy)
                x_margin = enemies_width / len(mixed_row)
            else:
                break
        x_shift = 0
        for index in range(len(mixed_row)):
            x_shift += x_margin
            enemy = mixed_row[index]
            enemy.rect.x = x_shift
            enemy.rect.y = y_margin + rows_above * y_margin * 2
            x_shift += enemy.rect.width
        return mixed_row

    # makes enemies from all given rows join the game
    def spawn_enemies(self, rows):
        for row in rows:
            for enemy in row:
                self.all_sprites.add(enemy)
                self.enemy_sprites.add(enemy)

    def check_collisions(self):
        hits = pygame.sprite.groupcollide(self.enemy_sprites, self.player_bullets, True, True)
        for hit in hits:
            hit.onDestroy()
            self.player_score.score_kill(hit)
            if len(self.enemy_sprites) == 0 and self.player.alive():
                self.manage_victory = True
                if self.current_level < Game.levels:
                    self.all_sprites.add(self.msg['lvl_completed'])
                    self.sounds['level_completed'].play()
                else:
                    self.all_sprites.add(self.msg['game_completed'])
                    self.sounds['game_completed'].play()
                self.player.fly_away()

        if not self.god_mode:
            hits = pygame.sprite.groupcollide(self.player_sprites, self.enemy_bullets, True, True)
            for hit in hits:
                hit.onDestroy()
                self.all_sprites.add(self.msg['player_killed'])
                self.manage_death = True
                self.player_score.score = 0

    # deletes sprites gone out of screen
    def delete_invisible(self):
        for entity in self.all_sprites:
            if entity.rect.bottom < 0 or entity.rect.top > Game.screen_res[1]:
                entity.kill()

    def manage_restart(self):
        if self.manage_death:
            self.can_restart = True
            if (not self.msg['player_killed'].alive()) and self.manage_death:
                prompt = Msg(self.screen, self.interface_font, 40, 50, 1, RGB.GREEN, "Press R to restart!", Msg.MSG_PULSE)
                self.all_sprites.add(prompt)
                self.manage_death = False
        elif self.manage_victory:
            self.manage_victory = False
            if self.current_level < Game.levels:
                self.current_level += 1
                self.running = False
            else:
                self.endgame_initiated = pygame.time.get_ticks()
        if self.endgame_initiated:
            now = pygame.time.get_ticks()
            if now - self.endgame_initiated > 7000:
                self.reset_progress()
                self.running = False

    def read_xml(self):
        xml_path = os.path.join(os.path.dirname(__file__), Game.lvl_desc_file)
        tree = et.parse(xml_path)
        lvl_name = "level_"+str(self.current_level)
        levels = tree.getroot()
        lvl = None
        for level in levels:
            if level.attrib['name'] == lvl_name:
                lvl = level
        rows_xml = lvl.find('rows')
        rows = []
        for row_xml in rows_xml:
            if row_xml.find('type').text == 'uniform':
                rows.append(self.get_uniform_row(eval(row_xml.find('enemy_class').text), len(rows)))
            elif row_xml.find('type').text == 'mixed':
                enemy_classes = []
                enemies_xml = row_xml.findall('enemy')
                for enemy_xml in enemies_xml:
                    (enemy_classes.append(eval(enemy_xml.text)))
                rows.append(self.get_mixed_row(enemy_classes, len(rows)))

        self.spawn_enemies(rows)
