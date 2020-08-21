import pygame

from ninja import Ninja

from pygame.sprite import Group

from settings import Settings

import game_functions as gf

from game_stats import GameStats

from button import Button

from scoreboard import Scoreboard


def run_game():
    
    
    pygame.init()

    
#Set Resolution
    mod_settings = Settings()
    screen = pygame.display.set_mode((mod_settings.screen_width, mod_settings.screen_height))

#Game caption
    pygame.display.set_caption("Masters of Death")

#Storing game statistics and scoreboard
    stats = GameStats(mod_settings)
    sb = Scoreboard(mod_settings, screen, stats)

#Make player ninja
    ninja = Ninja(mod_settings, screen)

#Star group
    stars = Group()

#Enemy Group
    enemies = Group()

#Slash Group max 1    
    slashes = Group()

#Powerup max 4
    powerups = Group()

#This 
    #gf.create_enemies(mod_settings, screen, ninja, enemies)

#Making play button
    play_button = Button(mod_settings, screen, "Play")

#Start main game loop
    while True:
        #Always check events so that we can click on the play button
        gf.check_events(mod_settings, screen, ninja, stars, slashes, powerups, stats, play_button, enemies, sb)

        #When the game is being played
        if stats.game_active:
            ninja.update()
            gf.update_powerups(mod_settings, ninja, powerups, stats)
            gf.update_stars(mod_settings, screen, ninja, enemies, stars, stats, sb)
            gf.update_enemies(mod_settings, enemies, stats, screen, ninja, stars, powerups, sb)
            gf.update_slashes(mod_settings, enemies, slashes, stats, sb)

        #Also always update the screen
        gf.update_screen(mod_settings, screen, ninja, enemies, stars, slashes, powerups, stats, play_button, sb)
        
        



run_game()
