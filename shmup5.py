# Etape 5 : amélioration des collisions
import pygame
import random
import os

img_dir = os.path.join(os.path.dirname(__file__), 'img')

# jeu vertical et rapide
WIDTH = 480
HEIGHT = 600
FPS = 60

# mes couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0) 
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.image = player_img
        # mais on préfère 2 fois plus petit
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pour debugger
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
            
        self.rect.x += self.speedx
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        
        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.image = pygame.Surface((30, 40))
        #self.image.fill(RED)
        self.image = meteor_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        # Etape 2 - amélioration avec speedx: 
        self.speedx = random.randrange(-3, 3)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)       

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #self.image = pygame.Surface((10, 20))
        #self.image.fill(YELLOW)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        # kill if it out of the screen
        if self.rect.bottom < 0:
            self.kill()
            

# Load game graphics
background = pygame.image.load(os.path.join(img_dir, "bg_1_1.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_dir, "playerShip1_orange.png")).convert()
meteor_img = pygame.image.load(os.path.join(img_dir, "meteorBrown_med1.png")).convert()
bullet_img = pygame.image.load(os.path.join(img_dir, "laserRed16.png")).convert()
            
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# boucle du jeu
running = True
while running:
    # keep looping at the right side
    clock.tick(FPS)
    
    # process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            
    # update
    all_sprites.update()
    
    # check if a bullet hits a mob (True, True => détruire les sprites)
    # retourne un dict de mobs 
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    
    # check collision
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits:
        running = False
        
    # render
    #screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    
    # after drawing everythong
    pygame.display.flip()

pygame.quit()