import pygame
import random
from os import path
import os
"""utilities for repetitive tasks used throughout various different modules"""


# loads from images folder
def load_image(file_name=None, rel_path='images'):
    if not file_name:
        file_name = random.choice(os.listdir(path.join(path.dirname(__file__), rel_path)))
    image = pygame.image.load(path.join(path.dirname(__file__), rel_path, file_name))
    return image


# loads from sounds folder
def load_sound(file_name=None):
    sound = pygame.mixer.Sound(path.join(path.dirname(__file__), 'sounds', file_name))
    return sound


class Colors:
    RED = (255, 0, 33)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)






