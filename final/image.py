# encoding: utf-8
import os
import pygame
from player import Player
from boss import Boss, BossBullet
from bullet import Bullet
from mobile import Mob
from explosion import Explosion
import powerup as Pwr
from shuttle import Shuttle
import global_parms as gp

background = None
background_rect = None
player_mini_img = None


def loadImages():
    global background, background_rect, player_mini_img
    
    # Load game graphics
    background = pygame.image.load(os.path.join(gp.img_dir, "bg_1_1.png")).convert()
    background_rect = background.get_rect()
    Player.player_img = pygame.image.load(os.path.join(gp.img_dir, "playerShip1_orange.png")).convert()
    
    # Charge les minis images du vaisseau pour compter le nb de vies
    player_mini_img = pygame.transform.scale(Player.player_img, (25, 19))
    player_mini_img.set_colorkey(gp.BLACK)
   
    Bullet.bullet_img = pygame.image.load(os.path.join(gp.img_dir, "laserRed16.png")).convert()

    meteor_images = []
    meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png',
                   'meteorBrown_med1.png', 'meteorBrown_med3.png',
                   'meteorBrown_small1.png', 'meteorBrown_small2.png',
                   'meteorBrown_tiny1.png', 'meteorBrown_tiny2.png']
    for img in meteor_list:
        meteor_images.append(pygame.image.load(os.path.join(gp.img_dir, img)).convert())
    Mob.meteor_images = meteor_images    
    
    Pwr.powerup_images = {
        Pwr.PWR_SHIELD: pygame.image.load(os.path.join(gp.img_dir, "shield_gold.png")).convert(),
        Pwr.PWR_GUN: pygame.image.load(os.path.join(gp.img_dir, "bolt_gold.png")).convert(),
        Pwr.PWR_XLIFE: pygame.image.load(os.path.join(gp.img_dir, "star_gold.png")).convert(),
    }
    
    # Chargement des images de l'explosion à 2 formats différents
    Explosion.explosion_anim = {}
    Explosion.explosion_anim['large'] = []
    Explosion.explosion_anim['small'] = []
    Explosion.explosion_anim['player'] = []
    
    for i in range(9):
        filename = f"regularExplosion0{i}.png"
        img = pygame.image.load(os.path.join(gp.img_dir, filename)).convert()
        img.set_colorkey(gp.BLACK)
        img_large = pygame.transform.scale(img, (75, 75))
        img_small = pygame.transform.scale(img, (32, 32))
        Explosion.explosion_anim['large'].append(img_large)
        Explosion.explosion_anim['small'].append(img_small)
    
        # Chargement animation
        filename = f"sonicExplosion0{i}.png"
        img = pygame.image.load(os.path.join(gp.img_dir, filename)).convert()
        img.set_colorkey(gp.BLACK)
        Explosion.explosion_anim['player'].append(img)
        
    Boss.boss_img = pygame.image.load(os.path.join(gp.img_dir, "boss.png")).convert()
    BossBullet.boss_bullet_img = pygame.image.load(os.path.join(gp.img_dir, "bullet.png")).convert()
    
    Shuttle.shuttle_right_img = pygame.image.load(os.path.join(gp.img_dir, "shuttle-right.png")).convert()
    Shuttle.shuttle_left_img = pygame.image.load(os.path.join(gp.img_dir, "shuttle-left.png")).convert()       
    