from pygame.sprite import Sprite
from pygame.sprite import Group
from ship_fragment import ShipFragment as sf
from explosion import Explosion
from utils import load_image
from utils import load_sound
import os
import random



class Mob(Sprite):
    """Abstract class representing every battleship on the screen"""

    def __init__(self, screen, config, spawn_x, spawn_y, all_sprites):
        super(Mob, self).__init__()

        self.screen = screen

        # LOAD ASSETS
        # mandatory
        self.config = config
        self.all_sprites = all_sprites
        self.image = load_image(config.img_file)
        self.death_sounds = []
        for death_file in config.death_sound_files:
            sound = load_sound(death_file)
            self.death_sounds.append(sound)
        self.explosion_animation = []
        for explosion_frame in range(self.config.explosion_frames):
            frame = load_image(self.config.explosion_img_prefix + str(explosion_frame) + '.png')
            self.explosion_animation.append(frame)

        # optional (but common)
        if hasattr(config, 'bullet_img_file'):
            self.bullet_image = load_image(config.bullet_img_file)
            self.shoot_sounds = []
        if hasattr(config, 'shoot_sound_files'):
            self.shoot_sounds = []
            for shoot_file in config.shoot_sound_files:
                sound = load_sound(shoot_file)
                self.shoot_sounds.append(sound)

        # get rects
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.rect.x = spawn_x
        self.rect.y = spawn_y

    def blitime(self):
        self.screen.blit(self.image, self.rect)

    def onDestroy(self):
        random.choice(self.death_sounds).play()
        self.all_sprites.add(Explosion(self.screen, self.explosion_animation, self.rect.centerx, self.rect.centery))
        for frag in self.getRandomDebries():
            self.all_sprites.add(frag)
        self.kill()

    def getRandomDebries(self, beams=3, particles=10, guns=1):
        debries = Group()
        x = self.rect.centerx
        y = self.rect.centery
        path1 = os.path.join('images', 'ship_fragments')

        if hasattr(self.config, "color"):
            color = self.config.color
            debries.add(sf(self.screen, load_image(rel_path=os.path.join(path1, color, 'cockpits')), x, y))
            debries.add(sf(self.screen, load_image(rel_path=os.path.join(path1, color, 'wings')), x, y))
            debries.add(sf(self.screen, load_image(rel_path=os.path.join(path1, color, 'wings')), x, y))
        for i in range(beams):
            debries.add(sf(self.screen, load_image(rel_path=os.path.join(path1, 'universal', 'beams')), x, y))
        for i in range(particles):
            debries.add(sf(self.screen, load_image(rel_path=os.path.join(path1, 'universal', 'particles')), x, y))
        for i in range(guns):
            debries.add(sf(self.screen, load_image(rel_path=os.path.join(path1, 'universal', 'guns')), x, y))
        return debries



