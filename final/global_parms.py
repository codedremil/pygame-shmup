# encoding: utf-8
# Paramètres globaux
# jeu vertical et rapide
import os
import pygame

# Difficultés du jeu
WIDTH = 480
HEIGHT = 600
FPS = 60
NB_MOB = 8
BOSS_DELAY = 10000
BOSS_MIN_SCORE = 500
SHUTTLE_DELAY = 7000
MAX_LIVES = 5

# mes couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0) 
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# les répertoires des ressources
game_dir = os.path.dirname(__file__)
img_dir = os.path.join(game_dir, 'img')
snd_dir = os.path.join(game_dir, 'snd')

# les groupes de Sprite
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
powerups = pygame.sprite.Group()
bossbullets = pygame.sprite.Group()
