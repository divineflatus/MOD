import pygame

#Class to store game statistics
class GameStats():
    def __init__(self, mod_settings):

        #Initialize MOD settings
        self.mod_settings = mod_settings

        #Number of lives available
        self.ninjas_left = self.mod_settings.ninja_limit

        #Starts inactive until 'Play' is clicked
        self.game_active = False

        #Resets statistics
        self.reset_stats()

        self.high_score = 0

    #Resets statistics to appropriate values
    def reset_stats(self):
        self.ninjas_left = self.mod_settings.ninja_limit
        self.score = 0
