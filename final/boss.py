# encoding: utf-8
import pygame
import random
import global_parms as gp

class Boss(pygame.sprite.Sprite):
    boss_img = None
    SPEED_X = 3
    SHOOT_DELAY = 500
    TIME_DELAY = 200
    
    def __init__(self, target, sound):
        super().__init__()
        self.target = target
        
        # mais on préfère 2 fois plus petit
        self.image = pygame.transform.scale(Boss.boss_img, (50, 38))
        self.image.set_colorkey(gp.BLACK)
        self.rect = self.image.get_rect()
        self.sound = sound
        
        # choisit le sens
        if random.randrange(2):
            self.rect.x = gp.WIDTH
            self.speedx = -Boss.SPEED_X
        else:
            self.rect.x = 0
            self.speedx = Boss.SPEED_X
            
        self.rect.centery = random.randrange(20 + int(gp.HEIGHT * 0.5))
        
        gp.all_sprites.add(self)
        now = pygame.time.get_ticks()
        self.shoot_time = now
        self.sound_time = now
        
        
    def update(self):
        self.rect.x += self.speedx
        # kill if it out of the screen
        if self.rect.x < 0 or self.rect.x > gp.WIDTH:
            self.kill()
            
        now = pygame.time.get_ticks()
        if now - self.shoot_time > Boss.SHOOT_DELAY:
            self.shoot_time = now
            self.shoot()
            
        if now - self.sound_time > Boss.TIME_DELAY:
            self.sound_time = now
            self.sound.play()
            
            
    def shoot(self):
        BossBullet(self, self.target)


class BossBullet(pygame.sprite.Sprite):
    boss_bullet_img = None
    
    def __init__(self, boss, target):
        super().__init__()
        self.image = BossBullet.boss_bullet_img
        self.image.set_colorkey(gp.BLACK)
        self.rect = self.image.get_rect()
        
        self.rect.x = boss.rect.x
        self.rect.y = boss.rect.y + 10
        self.pos = pygame.math.Vector2(self.rect.center)

        target = pygame.math.Vector2(target.rect.x, target.rect.y)
        start = pygame.math.Vector2(self.rect.x, self.rect.y)
        delta = target - start
        # distance = delta.length()
        direction = delta.normalize()
        self.velocity = direction * 6
        
        gp.all_sprites.add(self)
        gp.bossbullets.add(self)
        
        
    def update(self):
        self.pos = self.pos + self.velocity
        self.rect.center = (int(self.pos[0]), int(self.pos[1]))
        
        # kill if it out of the screen
        if self.rect.x < 0 or self.rect.x > gp.WIDTH or self.rect.y < 0 or self.rect.y > gp.HEIGHT:
            self.kill()          
        
        