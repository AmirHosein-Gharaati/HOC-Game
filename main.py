import sys
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pygame.locals import *

from pages.help_page import HelpPage
from pages.main_page import MainPage
from pages.play_menu_page import PlayMenuPage

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1022, 700))
        pygame.display.set_caption("15")
        
        self.mainPage = MainPage(self.screen)
        self.helpPage = HelpPage(self.screen)
        self.playMenuPage = PlayMenuPage(self.screen)
        
    def run(self):
        situation = "Main"
        while situation != "Exit":
            if situation == "Main":
                self.mainPage.show()
                situation = self.mainPage.run()
            
            elif situation == "Help":
                self.helpPage.show()
                situation = self.helpPage.run()
            
            elif situation == "Play":
                self.playMenuPage.show()
                situation = self.playMenuPage.run()
        
        pygame.quit()

Game().run()
sys.exit(0)