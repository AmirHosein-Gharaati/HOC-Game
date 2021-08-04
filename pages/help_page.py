import pygame
from pygame.locals import QUIT

from .components.button import Button
from .components.color import Color
from .components.font import Font

class HelpPage:
    def __init__(self, screen):
        self.screen = screen
        self.initializeImages()
        self.initializeButtons()
        
    
    def initializeButtons(self):
        self.mainPageButton = Button(self.screen, (445, 512, 132, 44), Color.RED, Color.BLACK, Font.make("Garamond", 30), "Main Page", "Main")
    
    def initializeImages(self):
        self.mainBackgroundImage = pygame.image.load("images/MainBackground.png")

    def show(self):
        self.screen.blit(self.mainBackgroundImage, (0, 0))
        self.screen.blit(Font.make("Algerian", 116).render("FIFTEEN", 1, Color.BLACK), (290, 0))
        self.mainPageButton.show()
        
        pygame.display.flip()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "Exit"
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mainPageButton.collidepoint(pygame.mouse.get_pos()):
                        return "Main"