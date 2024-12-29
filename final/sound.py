# encoding: utf-8
import os
import pygame
import global_parms as gp

shoot_sound = None
boss_sound = None
shield_sound = None
power_sound = None
explosion_sounds = []
shield_explosion = None
player_die_sound = None

def loadSounds():
    global shoot_sound, shield_sound, power_sound, explosion_sounds
    global player_die_sound, boss_sound, shield_explosion
    pygame.mixer.init()

    # Chargement des sons    
    shoot_sound = pygame.mixer.Sound(os.path.join(gp.snd_dir, "shoot.wav"))
    shoot_sound.set_volume(0.5)
    boss_sound = pygame.mixer.Sound(os.path.join(gp.snd_dir, "boss.wav"))
    shield_explosion = pygame.mixer.Sound(os.path.join(gp.snd_dir, "shield_expl.wav"))
    
    # 2 sons de plus
    shield_sound = pygame.mixer.Sound(os.path.join(gp.snd_dir, "pow4.wav"))
    power_sound = pygame.mixer.Sound(os.path.join(gp.snd_dir, "pow5.wav"))
    for snd in ['expl1.wav', 'expl2.wav']:
        sound = pygame.mixer.Sound(os.path.join(gp.snd_dir, snd))
        explosion_sounds.append(sound)
        sound.set_volume(0.5)

    # Chargement du son quand le vaisseau explose
    player_die_sound = pygame.mixer.Sound(os.path.join(gp.snd_dir, 'rumble1.ogg'))
    
    pygame.mixer.music.load(os.path.join(gp.snd_dir, 
                                     'PetterTheSturgeon - Last_Knight_Of_The_CyberDeath.mp3'))

    pygame.mixer.music.set_volume(0.4)
    #pygame.mixer.music.play(loops=-1)
