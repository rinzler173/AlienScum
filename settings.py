from os import path
import pygame

"""Stores most crucial game settings"""

# environment settings
screen_res = 1344, 756
class Game:
    screen_res = 1344, 756  # full hd * 0,7
    caption = 'Alien Scum'
    background_img_file = 'background.png'
    interface_font_name = 'arial'
    lvl_desc_file = "levels.xml"
    levels = 3
    FPS = 60
    god_mode = True  # for testing only
    min_expl_vel = -10
    max_expl_vel = 10
    min_expl_rot = -8
    max_expl_rot = 8


# player settings
class Config:
    color = 'green'
    img_file = 'player_1.png'
    bullet_img_file = 'player_laser.png'
    shoot_sound_files = ['player_laser_1.wav']
    death_sound_files = ['player_death_1.wav']
    explosion_anim_dir = 'explosion_1'
    jet_anim_dir = 'jet_1'
    speed = 7.5
    bullet_speed = 100.0
    vertical_leeway = screen_res[1] * .015
    horizontal_margin = screen_res[0] * .02
    bottom_margin = screen_res[1] * .03


class BasicDroneConfig:
    color = 'red'
    img_file = 'basic_drone.png'
    bullet_img_file = 'red_laser_1.png'
    explosion_anim_dir = 'explosion_1'
    speed = 0
    bullet_speed = 5.0
    fire_rate = 1.5  # shots per second
    skipped_shots = 0.5  # odds of skipping a shot
    y_speed = 2.0
    death_sound_files = ['explosion_1.wav', 'explosion_2.wav']
    shoot_sound_files = ['enemy_laser_1.wav']
    value = 1


class TrishotDroneConfig:
    color = 'red'
    img_file = 'trishot_drone.png'
    bullet_img_file = 'red_laser_2.png'
    explosion_anim_dir = 'explosion_1'
    speed = 0
    bullet_speed = 15.0
    fire_rate = 1.0  # shots per second
    skipped_shots = 0.5  # odds of skipping a shot
    y_speed = 2.0
    death_sound_files = ['explosion_1.wav', 'explosion_2.wav']
    shoot_sound_files = ['enemy_laser_1.wav']
    value = 2


class BomberDroneConfig:
    color = 'red'
    img_file = 'bomber_drone.png'
    bullet_img_file = 'bomb_1.png'
    bullet_frames = ['bomb_1.png', 'bomb_2.png', 'bomb_3.png', 'bomb_4.png']
    explosion_anim_dir = 'explosion_1'
    speed = 0
    bullet_speed = 7.0
    fire_rate = 1.0  # shots per second
    skipped_shots = 0.5  # odds of skipping a shot
    y_speed = 2.0
    death_sound_files = ['explosion_1.wav', 'explosion_2.wav']
    shoot_sound_files = ['enemy_laser_1.wav']
    value = 2


class UfoConfig:
    img_file = 'ufo.png'
    bullet_img_file = 'guided_missile.png'
    shoot_sound_files = ['explosion_3.wav', 'explosion_4.wav']
    explosion_anim_dir = 'explosion_1'
    speed = 0
    bullet_speed = 7.0
    fire_rate = 1
    skipped_shots = 0.5
    y_speed = 3.0
    death_sound_files = ['explosion_3.wav', 'explosion_4.wav']
    value = 3







