# encoding: utf-8
import pygame
import global_parms as gp
from bullet import Bullet
import sound as snd

class Player(pygame.sprite.Sprite):
    MAX_SHIELD = 100
    POWERUP_TIME = 5000
    SHOOT_DELAY = 250
    MAX_SHOOTS = 5
    
    player_img = None
    
    def __init__(self):
        super().__init__()
        # mais on préfère 2 fois plus petit
        self.image = pygame.transform.scale(Player.player_img, (50, 38))
        self.image.set_colorkey(gp.BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = gp.WIDTH / 2
        self.rect.bottom = gp.HEIGHT - 10
        self.speedx = 0
        self.shield = Player.MAX_SHIELD
        
        # Ajout d'un délai
        self.shoot_delay = Player.SHOOT_DELAY
        self.last_shot = pygame.time.get_ticks()
        self.shoot_count = 0
        
        # Ajout des vies et mécanique pour masquer le vaisseau temporairement
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
       
        self.power = 1  # powerup level
        self.power_timer = pygame.time.get_ticks()
        
        gp.all_sprites.add(self)
        
        
    def update(self):
        # Timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > Player.POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
            
        # Il faut démasquer si le temps de masquage est révolu
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = gp.WIDTH / 2
            self.rect.bottom = gp.HEIGHT - 10
            
        self.speedx = 0
        
        # Traitement des actions
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
            
        self.rect.x += self.speedx
        
        if self.rect.right > gp.WIDTH:
            self.rect.right = gp.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
        
    def shoot(self):
        # pas de tir si on est caché
        if self.hidden:
            return
        
        now = pygame.time.get_ticks()

        # TODO: implémenter un algo du type : 5 tirs toutes les 2 secondes
        if now - self.last_shot > self.shoot_delay * 5:
            self.shoot_count = 0
            
        if self.shoot_count == Player.MAX_SHOOTS:
            if now - self.last_shot < self.shoot_delay * 5:
                return
            
            self.shoot_count = 0
            
        if now - self.last_shot < self.shoot_delay:
            return
        
        self.last_shot = now
        self.shoot_count += 1
 
        if self.power == 1:
            Bullet(self.rect.centerx, self.rect.top)
            snd.shoot_sound.play()
 
        if self.power >= 2:
            Bullet(self.rect.left, self.rect.centery)
            Bullet(self.rect.right, self.rect.centery)
            snd.shoot_sound.play()
        
    # Ajout du masquage en déplaçant hors de l'écran (astuce !)
    # décrémente le nombre de vies et raz des propriétés
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (gp.WIDTH / 2, gp.HEIGHT + 200)
        self.lives -= 1
        self.shield = Player.MAX_SHIELD
        self.power = 1
        
