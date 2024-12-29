# Etape 10 : ajout des explosions
# on va ajouter un délai entre 2 tirs
import pygame
import random
import os

img_dir = os.path.join(os.path.dirname(__file__), 'img')
snd_dir = os.path.join(os.path.dirname(__file__), 'snd')

# jeu vertical et rapide
WIDTH = 480
HEIGHT = 600
FPS = 60
NB_MOB = 8
MAX_SHIELD = 100

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

font_name= pygame.font.match_font('arial')

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)   # True=>antialias
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, pourcent):
    #if pourcent < 0:
    #    pourcent = 0
        
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pourcent / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)   # épaisseur du trait
    
# Crée un nouveau mobile
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    

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
        self.shield = MAX_SHIELD
        
        # Ex-10: ajout d'un délai
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
            
        # On a déplacé l'appel à "shoot()" ici:
        if keystate[pygame.K_SPACE]:
            self.shoot()
            
        self.rect.x += self.speedx
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot < self.shoot_delay:
            return
        
        self.last_shot = now
        
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()
        
        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #si on ne fait pas une copie mais qu'on effectue une rotation
        #à chaque fois, on bouffe la mÃémoire et on perd la qualité de l'image
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        #self.rect.y = random.randrange(-100, -40)
        self.rect.y = random.randrange(-150, -100)  # à cause des big !
        self.speedy = random.randrange(1, 8)
        # Etape 2 - amÃ©lioration avec speedx: 
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        
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

class Explosion(pygame.sprite.Sprite):
    # On indique le point central de l'explosion et la taille (large ou small)
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
            

# Load game graphics
background = pygame.image.load(os.path.join(img_dir, "bg_1_1.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_dir, "playerShip1_orange.png")).convert()
#meteor_img = pygame.image.load(os.path.join(img_dir, "meteorBrown_med1.png")).convert()
bullet_img = pygame.image.load(os.path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png',
               'meteorBrown_med1.png', 'meteorBrown_med3.png',
               'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png', 'meteorBrown_tiny2.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_dir, img)).convert())

# Chargement des images de l'explosion Ã  2 formats diffÃ©rents
explosion_anim = {}
explosion_anim['large'] = []
explosion_anim['small'] = []
for i in range(9):
    filename = f"regularExplosion0{i}.png"
    img = pygame.image.load(os.path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_large = pygame.transform.scale(img, (75, 75))
    img_small = pygame.transform.scale(img, (32, 32))
    explosion_anim['large'].append(img_large)
    explosion_anim['small'].append(img_small)
    
shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, "shoot.wav"))
explosion_sounds = []
for snd in ['expl1.wav', 'expl2.wav']:
    explosion_sounds.append(pygame.mixer.Sound(os.path.join(snd_dir, snd)))

pygame.mixer.music.load(os.path.join(snd_dir, 'PetterTheSturgeon - Last_Knight_Of_The_CyberDeath.mp3'))
pygame.mixer.music.set_volume(0.4)
           
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(NB_MOB):
    newmob()

score = 0
pygame.mixer.music.play(loops=-1)

# boucle du jeu
running = True
while running:
    # keep looping at the right side
    clock.tick(FPS)
    
    # process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #elif event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_SPACE:
        #        player.shoot()
            
    # update
    all_sprites.update()
    
    # check if a bullet hits a mob (True, True => détruire les sprites)
    # retourne un dict de mobs 
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(explosion_sounds).play()
        
        # on dessine un grosse explosion
        expl = Explosion(hit.rect.center, 'large')
        all_sprites.add(expl)
        newmob()    # on regénère le mobile
    
    # check collision : puisqu'on a un bouclier, on ne doit pas disparaitre tout de suite !
    #hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    #if hits:
    #    running = False
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        # plus le mobile est gros, plus l'impact est important !
        player.shield -= hit.radius * 2
        
        # on dessin eune petite explosion
        expl = Explosion(hit.rect.center, 'small')
        all_sprites.add(expl)
        
        # le mobile a disparu: il faut le regénérer
        newmob()    # on en a profité pour factoriser le code
        if player.shield <= 0:
            running = False
        
    # render
    #screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    
    # On dessine la barre du bouclier
    draw_shield_bar(screen, 5, 5, player.shield)
       
    # after drawing everythong
    pygame.display.flip()

pygame.quit()