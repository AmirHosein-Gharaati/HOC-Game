import sys
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pygame.locals import *

from Pages.HelpPage import HelpPage
from Pages.MainPage import MainPage


class Game:
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((1022, 700))
        pygame.display.set_caption("15")
    
        self.mainPage = MainPage(self.screen)
        self.helpPage = HelpPage(self.screen)
        
    def run(self):
        situation = "Main"
        while situation != "Exit":
            if situation == "Main":
                self.mainPage.show()
                situation = self.mainPage.run()
            
            elif situation == "Help":
                self.helpPage.show()
                situation = self.helpPage.run()
            
            elif situation == "Human vs Human":
                situation = "Main"
            
            elif situation == "Human vs Agent":
                situation = "Main"
            
            elif situation == "Agent vs Agent":
                situation = "Main"
        
        pygame.quit()

Game().run()
sys.exit(0)