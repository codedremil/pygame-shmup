# encoding: utf-8

import pygame
import global_parms as gp


class Bullet(pygame.sprite.Sprite):
    bullet_img = None
    
    def __init__(self, x, y):
        super().__init__()
        self.image = Bullet.bullet_img
        self.image.set_colorkey(gp.BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        
        gp.all_sprites.add(self)
        gp.bullets.add(self)
        
    def update(self):
        self.rect.y += self.speedy
        # kill if it out of the screen
        if self.rect.bottom < 0:
            self.kill()
            
          