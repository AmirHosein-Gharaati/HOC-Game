import pygame
from pygame.locals import QUIT

from .Components.Button import Button
from .Components import Color

class HelpPage:
    def __init__(self, screen):
        self.screen = screen
        self.initializeFonts()
        self.initializeImages()
        self.initializeButtons()
        
    
    def show(self):
        self.screen.blit(self.mainBackgroundImage, (0, 0))
        
        self.screen.blit(self.Algerian116Font.render("FIFTEEN", 1, Color.BLACK), (290, 0))
        
        self.mainPageButton.show()
        
        pygame.display.flip()
    
    def initializeButtons(self):
        self.mainPageButton = Button((445, 512, 132, 44), Color.RED, "Main Page", self.Garamond30Font, self.screen)
    
    def initializeImages(self):
        self.mainBackgroundImage = pygame.image.load("images/MainBackground.png")
    
    def initializeFonts(self):
        self.Garamond30Font = pygame.font.Font("fonts/EBGaramond-VariableFont_wght.ttf", 30)
        self.Algerian116Font = pygame.font.Font("fonts/Algerian Regular.ttf", 116)
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "Exit"
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mainPageButton.collidepoint(pygame.mouse.get_pos()):
                        return "Main"