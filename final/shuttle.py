# encoding: utf-8
import pygame
import random
import global_parms as gp

class Shuttle(pygame.sprite.Sprite):
    shuttle_right_img = None
    shuttle_left_img = None
    
    SPEED_X = 2
    
    def __init__(self):
        super().__init__()
        
        # choisit le sens
        if random.randrange(2):
            self.image = Shuttle.shuttle_left_img
            self.rect = self.image.get_rect()
            self.rect.left = gp.WIDTH           
            self.speedx = -Shuttle.SPEED_X
        else:
            self.image = Shuttle.shuttle_right_img
            self.rect = self.image.get_rect()
            self.rect.right = 0
            self.speedx = Shuttle.SPEED_X            
            
        self.rect.centery = random.randrange(20 + int(gp.HEIGHT * 0.4))
        self.image.set_colorkey(gp.BLACK)
        #self.sound = sound
            
        gp.all_sprites.add(self)
        #now = pygame.time.get_ticks()
        
        
    def update(self):
        self.rect.x += self.speedx
        # kill if it out of the screen
        if self.rect.right < 0 or self.rect.left > gp.WIDTH:
            self.kill()
                                   