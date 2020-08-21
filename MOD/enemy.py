import pygame
import math
from pygame.sprite import Sprite

class Enemy(Sprite):

    def __init__(self, mod_settings, screen):

        super(Enemy, self).__init__()

        #Load the screen dimensions
        self.screen = screen
        
        #Load settings from settings file
        self.mod_settings = mod_settings

        #Empty list to store frames in
        self.images = []

        #Appends images to list
        self.images.append(pygame.image.load('catrun1.png').convert_alpha())
        self.images.append(pygame.image.load('catrun2.png').convert_alpha())
        self.images.append(pygame.image.load('catrun3.png').convert_alpha())
        self.images.append(pygame.image.load('catrun4.png').convert_alpha())
        self.images.append(pygame.image.load('catrun5.png').convert_alpha())
        self.images.append(pygame.image.load('catrun6.png').convert_alpha())

        #Create a counter to iterate through the frames
        self.counter = 0

        #Load the selected image
        self.image = self.images[self.counter]

        #Get enemy rectangle based on image dimensions
        self.rect = self.image.get_rect()

        #Find rectangle positions
        self.rect.x = mod_settings.screen_width - self.rect.width 
        self.rect.y = mod_settings.screen_height - self.rect.height

        #Actual x & y positions for the enemy
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        


    #Checks the edges of the enemy against the screen edges
    def check_edges(self):
        
        screen_rect = self.screen.get_rect()
        
        if self.rect.top < screen_rect.top:
            return True
        elif self.rect.bottom > screen_rect.bottom:
            return True
##
##        elif self.rect.right < screen_rect.left:  
##            
            


#Updates the enemy
    def update(self):
        
        #Increment the counter
        self.counter += 1

        #When the counter is longer than the number of images loaded it resets to 0
        if self.counter >= len(self.images):
            self.counter = 0

        #Loads the right image based on incremented counter    
        self.image = self.images[self.counter]

        #Updates x position and rectangle
        self.x -= (self.mod_settings.enemy_speed * 0.5)
        self.rect.x = self.x

        #Updates y position and rectangle
        self.y +=(self.mod_settings.enemy_speed * self.mod_settings.group_direction)
        self.rect.y = self.y

    #Draws the enemy to the screen
    def blitme(self):
        self.screen.blit(self.image, self.rect)

           
