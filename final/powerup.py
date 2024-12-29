# encoding: utf-8
import pygame
import random
import global_parms as gp

PWR_SHIELD = 'shield'
PWR_GUN = 'gun'
PWR_XLIFE = 'xlife'

powerup_images = []
    
class Pow(pygame.sprite.Sprite):    
    def __init__(self, center):
        super().__init__()
        choice = random.random()
        if choice > 0.98:
            self.type = PWR_XLIFE
        else:
            self.type = random.choice([PWR_SHIELD, PWR_GUN])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(gp.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        #self.speedy = -10
        self.speedy = 3
        
    def update(self):
        self.rect.y += self.speedy
        # kill if it out of the screen
        #if self.rect.bottom < 0:
        if self.rect.top > gp.HEIGHT:
            self.kill()    
