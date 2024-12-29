# encoding: utf-8
import pygame
import random
from player import Player
from boss import Boss
from shuttle import Shuttle
from mobile import Mob
from explosion import Explosion
import powerup as Pwr
from powerup import Pow
import global_parms as gp
import sound as snd
import image as img
import highscore
import time



pygame.init()
screen = pygame.display.set_mode((gp.WIDTH, gp.HEIGHT))
pygame.display.set_caption("Shmup")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

img.loadImages()
snd.loadSounds()


death_explosion = None

def player_dead(where_rect, expl_type):
    global death_explosion
    
    death_explosion = Explosion(where_rect, expl_type)
    gp.all_sprites.add(death_explosion)
    snd.player_die_sound.play()
    player.hide()
    
    
def draw_text(surface, text, size, x, y, center=True):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, gp.WHITE)   # True=>antialias
    text_rect = text_surface.get_rect()
    if center:
        text_rect.midtop = (x, y)
    else:
        text_rect.left = x 
        text_rect.top = y
        
    surface.blit(text_surface, text_rect)


def draw_shield_bar(surface, x, y, pourcent):
    #if pourcent < 0:
    #    pourcent = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pourcent / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, gp.GREEN, fill_rect)
    pygame.draw.rect(surface, gp.WHITE, outline_rect, 2)   # épaisseur du trait
   
    
# Affichage des vies
def draw_lives(surf, lives, img):
    x = gp.WIDTH - 10 - (lives * 30)
    y = 5
    for i in range(lives):
        img_rect = img.get_rect()
        # 30 pixels car la mini image fait 25 (voir plus bas)
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
        
        
# Demande le nom du joueur
def ask_name():
    #question = "Indiquez votre nom: "
    #draw_text(screen, question, 40, gp.WIDTH / 2, 300)
    #pygame.display.flip()
    #pygame.display.update()
    font = pygame.font.Font(font_name, 40)

    question = "Indiquez votre nom: "
    question_img = font.render(question, True, gp.WHITE)
    question_rect = question_img.get_rect()
    question_rect.midtop = (gp.WIDTH / 2, 300)
    
    name = ''
    name_img = font.render(name, True, gp.WHITE)
    name_rect = name_img.get_rect()
    name_rect.topleft = (gp.WIDTH / 2 - 50, 350)
    cursor = pygame.Rect(name_rect.topright, (3, name_rect.height))

    in_progress = True
    while in_progress:
        question = "Indiquez votre nom: "
        draw_text(screen, question, 40, gp.WIDTH / 2, 300)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    in_progress = False
                elif event.key <= 127:
                    name += event.unicode
            
                name_img = font.render(name, True, gp.WHITE)
                name_rect.size = name_img.get_size()
                cursor.topleft = name_rect.topright
           
        screen.blit(img.background, img.background_rect)
        screen.blit(question_img, question_rect) 
        screen.blit(name_img, name_rect)
        if time.time() % 1 > 0.5:
            pygame.draw.rect(screen, gp.WHITE, cursor)
        
        pygame.display.update()
        
    pygame.time.delay(1000)
    pygame.event.clear()
            
    return name


# Affichage des règles
def display_rules():
    screen.blit(img.background, img.background_rect)
    draw_text(screen, "SHMUP!", 64, gp.WIDTH / 2, 30)
    draw_text(screen, "Flèches pour se déplacer, <espace> pour tirer", 18, 55, 130, False)
    image = pygame.transform.scale(Player.player_img, (25, 19))
    image.set_colorkey(gp.BLACK)
    screen.blit(image, (20, 134))

    draw_text(screen, "Recharge le bouclier", 18, 55, 170, False)
    image = pygame.transform.scale(Pwr.powerup_images[Pwr.PWR_SHIELD], (25, 25))
    image.set_colorkey(gp.BLACK)
    screen.blit(image, (20, 174))
    
    draw_text(screen, "Double le nombre de tirs", 18, 55, 210, False)
    image = pygame.transform.scale(Pwr.powerup_images[Pwr.PWR_GUN], (25, 25))
    image.set_colorkey(gp.BLACK)
    screen.blit(image, (20, 214))
    
    draw_text(screen, "Donne une vie supplémentaire", 18, 55, 250, False)
    image = pygame.transform.scale(Pwr.powerup_images[Pwr.PWR_XLIFE], (25, 25))
    image.set_colorkey(gp.BLACK)
    screen.blit(image, (20, 254))
    
    draw_text(screen, "Les météorites détruisent le vaisseau", 18, 55, 310, False)
    image = pygame.transform.scale(Mob.meteor_images[0], (25, 25))
    image.set_colorkey(gp.BLACK)
    screen.blit(image, (20, 314))
    
    draw_text(screen, "Le Boss essaye de vous détruire !", 18, 55, 350, False)
    image = pygame.transform.scale(Boss.boss_img, (25, 25))
    image.set_colorkey(gp.BLACK)
    screen.blit(image, (20, 354))
    
    draw_text(screen, "Vous avez perdu si vous détruisez la Navette !", 18, 55, 390, False)
    image = pygame.transform.scale(Shuttle.shuttle_right_img, (25, 25))
    image.set_colorkey(gp.BLACK)
    screen.blit(image, (20, 394))
    
    draw_text(screen, "Appuyez sur <Entrée> pour commencer", 18, gp.WIDTH / 2, gp.HEIGHT - 60)
    
    #pygame.display.flip()
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(gp.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            #if event.type == pygame.KEYUP and 
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_RETURN]:
                waiting = False


# Affichage du Game Over
def display_game_over():
    if highscore.is_highscore(score):
        player_name = ask_name()
        highscore.update(player_name, score)

        
def show_game_over_screen():
    screen.blit(img.background, img.background_rect)
    draw_text(screen, "SHMUP!", 64, gp.WIDTH / 2, 30)
    draw_text(screen, "Appuyez sur la touche <R> pour obtenir les règles", 18, 
              gp.WIDTH / 2, 130)
    draw_text(screen, "Appuyez sur <Entrée> pour commencer", 18, 
              gp.WIDTH / 2, 180)
    
    # Affiche les scores
    draw_text(screen, "Tableau des meilleurs scores :", 24, gp.WIDTH / 2, gp.HEIGHT / 2 - 60)
    scores = highscore.load_high_score()
    scores = scores['scores']
    for idx, score in enumerate(scores):
        draw_text(screen, score['nom'], 22, 100, gp.HEIGHT / 2 + 30 * (idx+1) - 40, False)
        draw_text(screen, str(score['score']), 22, 300 , gp.HEIGHT / 2 + 30 * (idx+1) - 40, False)
    
    #pygame.display.flip()
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(gp.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            #if event.type == pygame.KEYUP and 
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_r]:
                display_rules()
                continue
            
            if keystate[pygame.K_RETURN]:
                waiting = False

# boucle du jeu
game_over = True
running = True

while running:
    if game_over:
        show_game_over_screen() # l'utilisateur presse une touche
        game_over = False
        # refactoring necessaire pour reinitialiser les variables
        gp.all_sprites = pygame.sprite.Group()
        gp.mobs = pygame.sprite.Group()
        gp.bullets = pygame.sprite.Group()
        gp.powerups = pygame.sprite.Group()
        player = Player()
        for i in range(gp.NB_MOB):
            Mob()
        
        score = 0
        last_time_boss = pygame.time.get_ticks()
        last_time_shuttle = pygame.time.get_ticks()
        shuttle = None
        boss = None
        
    # keep looping at the right side
    clock.tick(gp.FPS)
    
    # process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # update
    gp.all_sprites.update()
    
    # check if a bullet hits a mob (True, True => détruire les sprites)
    # retourne un dict de mobs 
    hits = pygame.sprite.groupcollide(gp.mobs, gp.bullets, True, True)
    for hit in hits:
        # radius max is 54 !
        score += 55 - hit.radius
        random.choice(snd.explosion_sounds).play()
        
        # on dessine un grosse explosion
        expl = Explosion(hit.rect.center, 'large')
        gp.all_sprites.add(expl)
        # on génère un powerup mais pas tout le temps
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            gp.all_sprites.add(pow)
            gp.powerups.add(pow)
            
        Mob()    # on regénère le mobile
        
    # teste si le boss a été touché
    if boss:
        hits = pygame.sprite.spritecollide(boss, gp.bullets, True)
        for hit in hits:
            random.choice(snd.explosion_sounds).play()
        
            # on dessine un grosse explosion
            if boss:
                expl = Explosion(hit.rect.center, 'large')
                boss.kill()
                boss = None
        
    # si un tir a touché la navette le jeu est fini
    if shuttle:
        hits = pygame.sprite.spritecollide(shuttle, gp.bullets, True)
        for hit in hits:
            if shuttle:
                expl = Explosion(hit.rect.center, 'large')
                gp.all_sprites.add(expl)
                snd.player_die_sound.play()
                shuttle.kill()
                shuttle = None
                player_dead(player.rect.center, 'large')
    
    # check collision : puisqu'on a un bouclier, on ne doit pas disparaitre tout de suite !
    #hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    hits = pygame.sprite.spritecollide(player, gp.mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        # plus le mobile est gros, plus l'impact est important !
        player.shield -= hit.radius * 2
        
        # on dessine une petite explosion
        expl = Explosion(hit.rect.center, 'small')
        gp.all_sprites.add(expl)
        snd.shield_explosion.play()
        
        # le mobile a disparu: il faut le regénérer
        Mob()
        if player.shield <= 0:
            player_dead(player.rect.center, 'player')
            
    # Vérifie les collisions avec les bossbullets
    hits = pygame.sprite.spritecollide(player, gp.bossbullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        # pas de bouclier: mort immédiate
        # on dessine une petite explosion
        expl = Explosion(hit.rect.center, 'small')
        gp.all_sprites.add(expl)
        player_dead(player.rect.center, 'player')
            
    # teste si le joueur a touché un powerup
    hits = pygame.sprite.spritecollide(player, gp.powerups, True)
    for hit in hits:
        if hit.type == Pwr.PWR_SHIELD:
            player.shield += random.randrange(10, 20)
            snd.shield_sound.play()
            if player.shield >= Player.MAX_SHIELD:
                player.shield = Player.MAX_SHIELD
        elif hit.type == Pwr.PWR_GUN:   # on veut 2 bullets !
            player.powerup()
            snd.power_sound.play()
        elif hit.type == Pwr.PWR_XLIFE:
            if player.lives < gp.MAX_LIVES:
                player.lives += 1
            
    # si le joueur est mort ET l'explosion est finie
    # dans une 2ème version, on teste plutôt le nb de vies
    if player.lives <= 0 and not death_explosion.alive():
        display_game_over()
        game_over = True
          
    # affiche un boss toutes les 10s après 500 points 
    now = pygame.time.get_ticks()
    if now - last_time_boss > gp.BOSS_DELAY and score > gp.BOSS_MIN_SCORE:
        boss = Boss(player, snd.boss_sound)
        last_time_boss = now
        
        # et crée un nouveau mobile
        Mob()
        
    # affiche une navette toutes les 6s
    if now - last_time_shuttle > gp.SHUTTLE_DELAY:
        shuttle = Shuttle()
        last_time_shuttle = now
        
    # render
    screen.blit(img.background, img.background_rect)
    gp.all_sprites.draw(screen)
    draw_text(screen, str(score), 18, gp.WIDTH / 2, 10)
    
    # On dessine la barre du bouclier
    draw_shield_bar(screen, 5, 5, player.shield)
    
    # Affichage des vies:
    draw_lives(screen, player.lives, img.player_mini_img)
       
    # after drawing everythong
    pygame.display.flip()

pygame.quit()
