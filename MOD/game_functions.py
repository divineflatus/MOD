import pygame

import sys

import time, datetime

from stars import Star

from slash import Slash

from enemy import Enemy

from powerup import Power

from pygame.sprite import Group

from random import choice, uniform

from time import sleep

#Check all events
def check_events(mod_settings, screen, ninja, stars, slashes, powerups, stats, play_button, enemies, sb):

    for event in pygame.event.get():  #For exiting
        if event.type == pygame.QUIT:
            quit()
            
        #Separate checks for keydown, keyup, and mouse clicks
        elif event.type == pygame.KEYDOWN: 
            check_keydown_events(event, mod_settings, screen, ninja, stars, slashes, powerups)
            
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ninja)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, mod_settings, screen, ninja, enemies, stars, slashes, sb)

            
#Key down events
def check_keydown_events(event, mod_settings, screen, ninja, stars, slashes, powerups):

    if event.key == pygame.K_w: #w
        ninja.moving_up = True
    if event.key == pygame.K_s: #s
        ninja.moving_down = True
    if event.key == pygame.K_SPACE: #Space
        throw_star(mod_settings, screen, ninja, stars)
    if event.key == pygame.K_d: #d
        slash(mod_settings, screen, ninja, slashes)

    #This controls the spawning of powerups. If a player does not hit any keys, no
    #powerups will spawn. We randomly generate a number on keypresses and when it
    #matches 'spawn' it will create a powerup
    spawn = 1
    yesorno = choice(range(10))

    if spawn == yesorno:
        power(mod_settings, screen, ninja, powerups)

        

    
#Key up events
def check_keyup_events(event, ninja):

    if event.key == pygame.K_w: #w
        ninja.moving_up = False
    if event.key == pygame.K_s: #s
        ninja.moving_down = False
    if event.key == pygame.K_SPACE: #space      sets ninja throw to false
        ninja.throwing = False
        ninja.image = ninja.idle
    if event.key == pygame.K_d: #d      sets ninja slash to false
        ninja.slashing = False
        ninja.image = ninja.idle


#Updates screen
def update_screen(mod_settings, screen, ninja, enemies, stars, slashes, powerups, stats, play_button, sb):

    #Update background
    clock = pygame.time.Clock()

    screen.fill((230,230,230))

    screen.blit(mod_settings.bg, (0, 0))

    #draw ninja
    ninja.blitme()

    #draw enemy group to screen
    enemies.draw(screen)

    #draw powerup group to screen (only one at a time)
    for power in powerups.sprites():
        power.draw_powerup()
        
    #draw star group to screen
    for star in stars.sprites():
        star.draw_star(ninja)

    #Display the current score
    sb.show_score()

    #Draws play button before game starts
    if not stats.game_active:
        play_button.draw_button()

        
    #Display most recent screen
    pygame.display.flip()

    #Sets the framerate
    clock.tick(60)

    


#Updates the star group
def update_stars(mod_settings, screen, ninja, enemies, stars, stats, sb):

    stars.update()

    #checks for active piercing powerup, boolean value
    piercing = mod_settings.piercing

    #makes a copy of group stars to check and see if star is beyond edge of screen
    #if so, it is deleted from the group
    for star in stars.copy():
        if star.rect.left > 1450:
            stars.remove(star)

    #Check for collision with enemies, if piercing is set to False, the star is not deleted on impact and can hit other enemies
    collisions = pygame.sprite.groupcollide(stars, enemies, piercing, True)

    #Increments the score
    if collisions:
        for enemies in collisions.values():
            stats.score += mod_settings.enemy_points
            sb.prep_score()
            sb.show_score()
        check_high_score(stats, sb)
    #When the enemies group is empty, we reset certain values and start the next wave. Enemy speed is incrememented by a speed scalar in settings
    if len(enemies) == 0:
        stars.empty()
        create_enemies(mod_settings, screen, ninja, enemies)
        mod_settings.enemy_speed += mod_settings.speed_scale
        mod_settings.ninja_speed = 10
        mod_settings.piercing = True
        mod_settings.stars_allowed = 5
        
#Throws stars    
def throw_star(mod_settings, screen, ninja, stars):
       
    #Spawns star if there are available slots in the group and plays the sound when created
    if len(stars) < mod_settings.stars_allowed:
        new_star = Star(mod_settings, screen, ninja)
        stars.add(new_star)
        ninja.starsound.play()
        #Set ninja throwing to true so appropriate frames are drawn in animation
        ninja.throwing = True

#Creates slashes
def slash(mod_settings, screen, ninja, slashes):

    #Only one slash allowed at a time
    if len(slashes) < 1:
        new_slash = Slash(mod_settings, screen, ninja)
        slashes.add(new_slash)
        #Play slash sound
        ninja.slashhit.play()
        #Set ninja slashing to true so appropriate frames are drawn in animation
        ninja.slashing = True
        
#Updates slashes group   
def update_slashes(mod_settings, enemies, slashes, stats, sb):

    slashes.update()

    #This removes slashes after rectangle moves beyond edge of ninja
    for slash in slashes.copy():
        if slash.rect.left > 60:
            slashes.remove(slash)

    #Checks for slash collisions
    hits = pygame.sprite.groupcollide(slashes, enemies, True, True)

    #Increments score for hit enemies. Double score for slashes
    if hits:
        for enemies in hits.values():
            stats.score += (mod_settings.enemy_points * 2)
            sb.prep_score()
            sb.show_score()
        check_high_score(stats, sb)


#Create powerups
def power(mod_settings, screen, ninja, powerups):

    #Only one powerup allowed at a time. If created added to group.
    if len(powerups) < 1:
        new_power = Power(mod_settings, screen, ninja)
        powerups.add(new_power)
            
#Calculates and returns the number of enemies that can fit on the screen
def get_number_enemies(mod_settings, enemy_height):

    available_space_y = mod_settings.screen_height - 2 * enemy_height
    
    number_enemies_y = int(available_space_y /(2 * enemy_height))
    
    return number_enemies_y


#Creates a single enemy with the values determined in get_number_cols and create_enemies
def create_enemy(mod_settings, screen, enemies, enemy_number, col_number):

    #Appropriate enemy settings pulled from enemy class based on sprite dimensions
    enemy = Enemy(mod_settings, screen)
       
    enemy_width = enemy.rect.width
    enemy_height =  enemy.rect.height

    #Places enemy in appropriate 'x' location. uniform is used to randomly change the position so that the enemies are always placed in slightly different positions
    enemy.x = mod_settings.screen_width - (enemy_width + 2 * enemy_width * col_number * uniform(1.0, 1.5))

    #Adjusts the positioning of enemies to prevent them from spawning off screen
    if enemy.x < 100:
        enemy.x += 400

    #Places enemy in appropriate 'y' location. uniform is used to randomly change the position so that the enemies are always placed in slightly different positions
    enemy.y = mod_settings.screen_height - (enemy_height + 2 * enemy_height * enemy_number * uniform(1.0, 2.0))

    #Adjusts position so enemies are not placed off screen
    if enemy.y < 0:
        enemy.y *= -1

    #Adjusts enemy position even further
    if enemy.y > mod_settings.screen_height:
        enemy.y -= mod_settings.screen_height

    #Load enemy rects
    enemy.rect.x = enemy.x

    enemy.rect.y = enemy.y   

    #Add Enemy to enemies group
    enemies.add(enemy)

    



#Creates enemies group using information from other functions    
def create_enemies(mod_settings, screen, ninja, enemies):

    enemy = Enemy(mod_settings, screen)
    
    number_enemies_y = get_number_enemies(mod_settings, enemy.rect.width)

    number_cols = get_number_cols(mod_settings, ninja.rect.width, enemy.rect.width)

    
    for col_number in range(number_cols-1):
        for enemy_number in range(number_enemies_y):
            create_enemy(mod_settings, screen, enemies, enemy_number, col_number)


#Calculates and returns the number of columns of enemies that will fit on the screen
def get_number_cols(mod_settings, ninja_width, enemy_width):

    available_space_x = (mod_settings.screen_width - (3 * enemy_width) - ninja_width)

    number_cols = int(available_space_x / (2 * enemy_width))

    return number_cols

#Checks if enemies have reached the edge of the screen
def check_group_edges(mod_settings, enemies):

    for enemy in enemies.sprites():
        if enemy.check_edges():
            #If one of the enemies hit the edge change the direction of the whole group
            change_group_direction(mod_settings, enemies)
            break

#Reverses enemies vertical direction called above
def change_group_direction(mod_settings, enemies):
    for enemy in enemies.sprites():
        enemy.rect.x -= mod_settings.enemy_speed
    mod_settings.group_direction *= -1


    
#Updates enemies group  
def update_enemies(mod_settings, enemies, stats, screen, ninja, stars, powerups, sb):

    #Calls the group edge check function
    check_group_edges(mod_settings, enemies)
    enemies.update()

    #Checks if enemies have passed the left side of the screen
    check_enemies_left(mod_settings, stats, screen, ninja, enemies, stars, powerups, sb)

    #Checks for collision with the ninja
    hits = pygame.sprite.spritecollideany(ninja, enemies)

    #When colliding with the ninja, call ninja hit
    if hits:
        ninja_hit(mod_settings, stats, screen, ninja, enemies, stars, powerups, sb)

#When an enemy hits the ninja or the left side of the screen this is called
def ninja_hit(mod_settings, stats, screen, ninja, enemies, stars, powerups, sb):


    #If there are lives remaining, decrement by one    
    if stats.ninjas_left > 0:
        stats.ninjas_left -= 1

        #To update the scoreboard            
        sb.prep_score()

        #Resets enemies, stars, and powerups group
        enemies.empty()
        stars.empty()
        powerups.empty()

        #Creates a new group of enemies
        create_enemies(mod_settings, screen, ninja, enemies)
        ninja.center_ninja()

        #Pauses the game for a moment
        sleep(0.5)
        
    #When there are no lives remaining
    elif stats.ninjas_left == 0:
        #Reset all statistics this is not rendered until the next call to update screen. We wait so that the score may be seen at the end of a game.
        stats.reset_stats()
        stats.score = 0
        stats.game_active = False

        #Resets values back to default
        mod_settings.ninja_speed = 6
        mod_settings.stars_allowed = 5
        mod_settings.enemy_speed = 2.5


#Checks for enemies passing the left side of the screen
def check_enemies_left(mod_settings, stats, screen, ninja, enemies, stars, powerups, sb):
    screen_rect = screen.get_rect()

    #Checks each enemy sprite and calls ninja_hit if they go off the edge
    for enemy in enemies.sprites():
        if enemy.rect.right < screen_rect.left:
            ninja_hit(mod_settings, stats, screen, ninja, enemies, stars, powerups, sb)
            break


#Powerups

#Slows enemies
def slowdown(mod_settings, powerups):
    
    mod_settings.enemy_speed *= .75

#Adds 1 life to player
def lifeup(mod_settings, powerups, stats):

    stats.ninjas_left += 1

#Increases player speed
def speedup(mod_settings, powerups):
    
    mod_settings.ninja_speed = 18

#Makes piercing stars by changing boolean value to false       
def piercing(mod_settings, powerups):

    mod_settings.piercing = False

#Speeds up enemies    
def enemy_speedup(mod_settings, powerups):

    mod_settings.enemy_speed += .6 

#Updates the powerups group
def update_powerups(mod_settings, ninja, powerups, stats):

    powerups.update()

    for power in powerups.copy():
        if power.rect.left < -10:
            powerups.remove(power)

    morepower = pygame.sprite.spritecollideany(ninja, powerups)


    #Determines which powerup to call choice is randomly generated in powerups class
    if morepower:
        for power in powerups:
            if power.choice == 0:
                slowdown(mod_settings, powerups)
                powerups.remove(power)
                break
            elif power.choice == 1:
                lifeup(mod_settings, powerups, stats)
                powerups.remove(power)
                break
            elif power.choice == 2:
                speedup(mod_settings, powerups)
                powerups.remove(power)
                break
            elif power.choice == 3:
                piercing(mod_settings, powerups)
                powerups.remove(power)
                break
            elif power.choice == 4:
                enemy_speedup(mod_settings, powerups)
                powerups.remove(power)
                break
            
#Checks if play button has been clicked when clicked we empty all groups, create new enemies and recenter the player
def check_play_button(stats, play_button, mouse_x, mouse_y, mod_settings, screen, ninja, enemies, stars, slashes, sb):

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        
        enemies.empty()
        stars.empty()
        slashes.empty()

        create_enemies(mod_settings, screen, ninja, enemies)
        ninja.center_ninja()

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()