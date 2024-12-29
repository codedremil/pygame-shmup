# encoding: utf-8
import pygame


class Explosion(pygame.sprite.Sprite):
    explosion_anim = []
    
    # On indique le point central de l'explosion et la taille (large ou small)
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.image = Explosion.explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        #self.frame_rate = 50
        # ex11: on accélère les explosions
        self.frame_rate = 75
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(Explosion.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = Explosion.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                