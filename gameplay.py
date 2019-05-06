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
        Gameplay.save = shelve.open('game_save')
        Gameplay.running = True
        Gameplay.can_restart = False
        Gameplay.manage_death = False
        Gameplay.manage_victory = False
        Gameplay.god_mode = Game.god_mode
        Gameplay.current_level = Gameplay.save['current_level']
        Gameplay.sounds = {}
        Gameplay.msg = {}
        Gameplay.sounds['level_completed'] = utils.load_sound('level_completed.wav')
        Gameplay.sounds['game_completed'] = utils.load_sound('game_completed.wav')
        Gameplay.screen = pygame.display.set_mode(Game.screen_res)
        pygame.display.set_caption(Game.caption)
        Gameplay.interface_font = pygame.font.match_font(Game.interface_font_name)
        Gameplay.background_img = utils.load_image(Game.background_img_file)
        Gameplay.background_rect = Gameplay.background_img.get_rect()
        Gameplay.clock = pygame.time.Clock()

        # initialize sprites
        Gameplay.all_sprites = pygame.sprite.Group()
        Gameplay.enemy_bullets = pygame.sprite.Group()
        Gameplay.enemy_sprites = pygame.sprite.Group()
        Gameplay.player_sprites = pygame.sprite.Group()
        Gameplay.player = Player(Gameplay.screen, Gameplay.all_sprites)
        Gameplay.player.add(Gameplay.all_sprites, Gameplay.player_sprites)
        Gameplay.player_score = ScoreCounter(Gameplay.player, Gameplay.save['player_score'], Gameplay.screen, Gameplay.interface_font, 25, RGB.BLACK)
        Gameplay.msg['game_completed'] = Msg(Gameplay.screen, Gameplay.interface_font, 65, 90, 1, RGB.GREEN,
                                             "Congratulations! Game completed!", Msg.MSG_PULSE)
        Gameplay.msg['lvl_completed'] = Msg(Gameplay.screen, Gameplay.interface_font, 100, 175, 2, RGB.GREEN, "Victory!", Msg.MSG_PULSE)
        Gameplay.msg['player_killed'] = Msg(Gameplay.screen, Gameplay.interface_font, 100, 175, 2, RGB.RED, "Game Over!", Msg.MSG_FADE)
        Gameplay.player_score.add(Gameplay.all_sprites)
        Gameplay.player_bullets = pygame.sprite.Group()

        Gameplay.enemy_rows = []
        Gameplay.read_xml(self)

    def run_gameplay(self):
        # Game loop
        while Gameplay.running:
            # handle events
            Gameplay.clock.tick(Game.FPS)
            Gameplay.check_events(self)
            Gameplay.manage_restart(self)
            # update sprites
            Gameplay.delete_invisible(self)
            Gameplay.all_sprites.update()
            Gameplay.check_colissions(self)
            # render graphics
            Gameplay.screen.blit(Gameplay.background_img, Gameplay.background_rect)
            Gameplay.all_sprites.draw(Gameplay.screen)
            pygame.display.flip()
        self.on_gameplay_stop()

    # save persistent data
    def on_gameplay_stop(self):
        Gameplay.save['current_level'] = Gameplay.current_level
        Gameplay.save['player_score'] = Gameplay.player_score.score

    def reset_progress(self):
        Gameplay.current_level = 1
        Gameplay.player_score.score = 0

    # all game loop inner functions below
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                Gameplay.on_keydown(self, event)
            elif event.type == pygame.KEYUP:
                Gameplay.on_keyup(self, event)
            elif event.type == pygame.QUIT:
                sys.exit()

    # manages key presses
    def on_keydown(self, event):
        if event.key in (pygame.K_LEFT, pygame.K_a):
            Gameplay.player.mov_flags['left'] = True
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            Gameplay.player.mov_flags['right'] = True
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            Gameplay.player.mov_flags['down'] = True
        elif event.key in (pygame.K_UP, pygame.K_w):
            Gameplay.player.mov_flags['up'] = True
        elif event.key == pygame.K_SPACE:
            bullet = Gameplay.player.shoot()
            Gameplay.all_sprites.add(bullet)
            Gameplay.player_bullets.add(bullet)
        elif event.key == pygame.K_r and Gameplay.can_restart:
            Gameplay.running = False


    # manages key releases
    def on_keyup(self, event):
        if event.key in (pygame.K_LEFT, pygame.K_a):
            Gameplay.player.mov_flags['left'] = False
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            Gameplay.player.mov_flags['right'] = False
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            Gameplay.player.mov_flags['down'] = False
        elif event.key in (pygame.K_UP, pygame.K_w):
            Gameplay.player.mov_flags['up'] = False

    # creates as many enemies of given class as can fit a single row
    # returns list representing the row
    # rows above argument should be combined height of all rows above (without margins)
    def get_uniform_row(self, enemy_class, rows_above):
        enemy = enemy_class(Gameplay.screen, 0, 0, Gameplay.all_sprites, Gameplay.enemy_bullets, Gameplay.enemy_sprites)
        y_margin = Gameplay.screen.get_rect().height * .09
        fittable_enemies = int(Gameplay.screen.get_rect().width / (enemy.rect.width * 2))
        uniform_row = []
        for index in range(fittable_enemies):
            uniform_row.append(enemy_class(Gameplay.screen, enemy.rect.width+(enemy.rect.width*2*index), y_margin + rows_above * y_margin * 2,
                                           Gameplay.all_sprites, Gameplay.enemy_bullets, Gameplay.enemy_sprites))
        return uniform_row

    def get_mixed_row(self, enemy_classes, rows_above):
        mixed_row = []
        y_margin = Gameplay.screen.get_rect().height * .09
        x_margin = 0
        screen_width = Gameplay.screen.get_rect().width
        enemies_width = 0
        for enemy_class in enemy_classes:
            if enemy_class == Ufo:
                enemy = enemy_class(Gameplay.screen, 0, 0, Gameplay.all_sprites, Gameplay.enemy_bullets, Gameplay.player, Gameplay.enemy_sprites)
            else:
                enemy = enemy_class(Gameplay.screen, 0, 0, Gameplay.all_sprites, Gameplay.enemy_bullets, Gameplay.enemy_sprites)
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
                Gameplay.all_sprites.add(enemy)
                Gameplay.enemy_sprites.add(enemy)

    def check_colissions(self):
        hits = pygame.sprite.groupcollide(Gameplay.enemy_sprites, Gameplay.player_bullets, True, True)
        for hit in hits:
            hit.onDestroy()
            Gameplay.player_score.score_kill(hit)
            if len(Gameplay.enemy_sprites) == 0:
                if Gameplay.current_level < Game.levels:
                    Gameplay.all_sprites.add(Gameplay.msg['lvl_completed'])
                    Gameplay.sounds['level_completed'].play()
                    Gameplay.manage_victory = True
                else:
                    Gameplay.all_sprites.add(Gameplay.msg['game_completed'])
                    Gameplay.sounds['game_completed'].play()
                    Gameplay.reset_progress(self)
                Gameplay.player.fly_away()

        if not Gameplay.god_mode:
            hits = pygame.sprite.groupcollide(Gameplay.player_sprites, Gameplay.enemy_bullets, True, True)
            for hit in hits:
                hit.onDestroy()
                Gameplay.all_sprites.add(Gameplay.msg['player_killed'])
                Gameplay.manage_death = True
                Gameplay.player_score.score = 0

    # deletes sprites gone out of screen
    def delete_invisible(self):
        for object in Gameplay.all_sprites:
            if object.rect.bottom < 0 or object.rect.top > Game.screen_res[1]:
                object.kill()

    def manage_restart(self):
        if Gameplay.manage_death:
            Gameplay.can_restart = True
            if (not Gameplay.msg['player_killed'].alive()) and Gameplay.manage_death:
                prompt = Msg(Gameplay.screen, Gameplay.interface_font, 40, 50, 1, RGB.GREEN, "Press R to restart!", Msg.MSG_PULSE)
                Gameplay.all_sprites.add(prompt)
                Gameplay.manage_death = False
        elif Gameplay.manage_victory:
            if not Gameplay.player.alive():
                if Gameplay.current_level < Game.levels:
                    Gameplay.current_level += 1
                Gameplay.running = False

    def read_xml(self):
        xml_path = os.path.join(os.path.dirname(__file__), Game.lvl_desc_file)
        tree = et.parse(xml_path)
        lvl_name = "level_"+str(Gameplay.current_level)
        levels = tree.getroot()
        lvl = None
        for level in levels:
            if level.attrib['name'] == lvl_name:
                lvl = level
        rows_xml = lvl.find('rows')
        rows = []
        for row_xml in rows_xml:
            if row_xml.find('type').text == 'uniform':
                rows.append(Gameplay.get_uniform_row(self, eval(row_xml.find('enemy_class').text), len(rows)))
            elif row_xml.find('type').text == 'mixed':
                enemy_classes = []
                enemies_xml = row_xml.findall('enemy')
                for enemy_xml in enemies_xml:
                    (enemy_classes.append(eval(enemy_xml.text)))
                rows.append(Gameplay.get_mixed_row(self, enemy_classes, len(rows)))

        Gameplay.spawn_enemies(self, rows)
            







