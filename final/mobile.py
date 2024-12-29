# encoding: utf-8
import pygame
import random
import global_parms as gp

class Mob(pygame.sprite.Sprite):
    meteor_images = []
    
    def __init__(self):
        super().__init__()

        #si on ne fait pas une copie mais qu'on effectue une rotation
        #à chaque fois, on bouffe la mémoire et on perd la qualité de l'image
        self.image_orig = random.choice(Mob.meteor_images)
        self.image_orig.set_colorkey(gp.BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        #print(f"radius={self.radius}, image={self.image_orig}")
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(gp.WIDTH - self.rect.width)
        #self.rect.y = random.randrange(-100, -40)
        self.rect.y = random.randrange(-150, -100)  # à cause des big !
        self.speedy = random.randrange(1, 8)
        # Etape 2 - amélioration avec speedx: 
        self.speedx = random.randrange(-3, 4)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 9)
        self.last_update = pygame.time.get_ticks()
        
        gp.all_sprites.add(self)
        gp.mobs.add(self)
        
        
    def _regenerate(self):
        self.rect.x = random.randrange(gp.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)  # à cause des big !
        self.speedy = random.randrange(1, 8)
        
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            # le pb c'est que le rectangle qui contient l'image doit s'adapter
            #self.image = pygame.transform.rotate(self.image_orig, self.rot)
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #if self.rect.top > gp.HEIGHT + 10 or self.rect.left < -25 or self.rect.right > gp.WIDTH + 20:
        if self.rect.top > gp.HEIGHT + 10 or self.rect.right < -5 or self.rect.left > gp.WIDTH + 5:
            self._regenerate()
            