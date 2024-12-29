# encoding: utf-8
# Etape 14 : game over & play again ?
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
POWERUP_TIME = 5000

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

font_name = pygame.font.match_font('arial')

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
    
# ex11: affichage des vies
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        # 30 pixels car la mini image fait 25 (voir plus bas)
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
        
# Céee un nouveau mobile
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
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = MAX_SHIELD
        
        # Ex-10: ajout d'un délai
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        
        # ex1: ajout des vies et mécanique pour masquer le vaisseau temporairement
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        # ex-13
        self.power = 1  # powerup level
        self.power_timer = pygame.time.get_ticks()
        
    def update(self):
        # ex13: timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
            
        # ex11: il faut démasquer si le temps de masquage est révolu
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            
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
        
    # ex-13
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot < self.shoot_delay or self.hidden:
            return
        
        self.last_shot = now
        # ex13
        if self.power == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
        if self.power >= 2:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2)
            shoot_sound.play()
        
    # ex11: ajout du masquage en déplaçant hors de l'écran (astuce !)
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
        
        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #si on ne fait pas une copie mais qu'on effectue une rotation
        #à chaque fois, on bouffe la mémoire et on perd la qualité de l'image
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        #print(f"radius={self.radius}, image={self.image_orig}")
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        #self.rect.y = random.randrange(-100, -40)
        self.rect.y = random.randrange(-150, -100)  # à cause des big !
        self.speedy = random.randrange(1, 8)
        # Etape 2 - amélioration avec speedx: 
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
            
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.type = random.choice(['shield', 'gun'])
        #self.image = bullet_img
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        #self.speedy = -10
        self.speedy = 3
        
    def update(self):
        self.rect.y += self.speedy
        # kill if it out of the screen
        #if self.rect.bottom < 0:
        if self.rect.top > HEIGHT:
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
        #self.frame_rate = 50
        # ex11: on accélère les explosions
        self.frame_rate = 75
        
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
            
 # ex14
def show_game_over_screen():
    # ex14: mettre en fin de TP pour montrer comment enjoliver
    screen.blit(background, background_rect)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Flèches pour se déplacer, <espace> pour tirer", 22, 
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Appuyez sur une touche pour commencer", 18, 
              WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Load game graphics
background = pygame.image.load(os.path.join(img_dir, "bg_1_1.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_dir, "playerShip1_orange.png")).convert()
#ex11: charge les minis images du vaisseau pour compter le nb de vies
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
#meteor_img = pygame.image.load(os.path.join(img_dir, "meteorBrown_med1.png")).convert()
bullet_img = pygame.image.load(os.path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png',
               'meteorBrown_med1.png', 'meteorBrown_med3.png',
               'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png', 'meteorBrown_tiny2.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_dir, img)).convert())

powerup_images = {
    'shield': pygame.image.load(os.path.join(img_dir, "shield_gold.png")).convert(),
    'gun': pygame.image.load(os.path.join(img_dir, "bolt_gold.png")).convert(),
}

# Chargement des images de l'explosion à 2 formats différents
explosion_anim = {}
explosion_anim['large'] = []
explosion_anim['small'] = []
# ex11: explosion du joueur
explosion_anim['player'] = []

for i in range(9):
    filename = f"regularExplosion0{i}.png"
    img = pygame.image.load(os.path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_large = pygame.transform.scale(img, (75, 75))
    img_small = pygame.transform.scale(img, (32, 32))
    explosion_anim['large'].append(img_large)
    explosion_anim['small'].append(img_small)
    # ex11: chargement animation
    filename = f"sonicExplosion0{i}.png"
    img = pygame.image.load(os.path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

# Chargement des sons    
shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, "shoot.wav"))
# ex13: 2 sons de plus
shield_sound = pygame.mixer.Sound(os.path.join(snd_dir, "pow4.wav"))
power_sound = pygame.mixer.Sound(os.path.join(snd_dir, "pow5.wav"))
explosion_sounds = []
for snd in ['expl1.wav', 'expl2.wav']:
    explosion_sounds.append(pygame.mixer.Sound(os.path.join(snd_dir, snd)))

# ex11: chargement du son quand le vaisseau explose
player_die_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'rumble1.ogg'))

pygame.mixer.music.load(os.path.join(snd_dir, 'PetterTheSturgeon - Last_Knight_Of_The_CyberDeath.mp3'))
pygame.mixer.music.set_volume(0.4)
           
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(NB_MOB):
    newmob()

score = 0
pygame.mixer.music.play(loops=-1)

# boucle du jeu
#ex 14
game_over = True
running = True
while running:
    if game_over:
        show_game_over_screen() # l'utilisateur presse une touche
        game_over = False
        # refactoring necessaire pour reinitialiser les variables
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(NB_MOB):
            newmob()
        
        score = 0
        
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
        # radius max is 54 !
        score += 55 - hit.radius
        random.choice(explosion_sounds).play()
        
        # on dessine un grosse explosion
        expl = Explosion(hit.rect.center, 'large')
        all_sprites.add(expl)
        # on génère un powerup mais pas tout le temps
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
            
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
            # ex11: quand le joueur meurt, on affiche une explosion !
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player_die_sound.play()
            player.hide()
            player.lives -= 1
            player.shield = 100
            player.power = 1
            
    # teste si le joueur a touché un powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 20)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':   # on veut 2 bullets !
            player.powerup()
            power_sound.play()
            
    # ex11: si le joueur est mort ET l'explosion est finie
    # dans une 2ème version, on teste plutôt le nb de vies
    #if not player.alive() and not death_explosion.alive():
    if player.lives == 0 and not death_explosion.alive():
        # ex14
        #running = False
        game_over = True
        
    # render
    #screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    
    # On dessine la barre du bouclier
    draw_shield_bar(screen, 5, 5, player.shield)
    
    # ex11: affichage des vies:
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
       
    # after drawing everythong
    pygame.display.flip()

pygame.quit()