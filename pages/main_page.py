import pygame

from pygame.locals import QUIT

from .components.button import Button
from .components.color import Color
from .components.font import Font

class MainPage:
    def __init__(self, screen):
        self.screen = screen
        self.initializeImages()
        self.initializeButtons()
    
    def initializeButtons(self):
        self.buttons = [
            Button(self.screen, (321, 320, 380, 70), Color.RED, Color.WHITE, Font.make("Garamond", 45), "Play"),
            Button(self.screen, (321, 420, 380, 70), Color.BLUE, Color.WHITE, Font.make("Garamond", 45), "Help")
        ]
    
    def initializeImages(self):
        self.mainBackgroundImage = pygame.image.load("images/backgrounds/MainBackground.png")
        self.card15Image = pygame.image.load("images/cards/15.png")
    
    def show(self):
        self.screen.blit(self.mainBackgroundImage, (0, 0))
        self.screen.blit(Font.make("Algerian", 116).render("FIFTEEN", 1, Color.BLACK), (290, 0))
        self.screen.blit(self.card15Image, (423, 121))
        
        for button in self.buttons:
            button.show()
        
        pygame.display.flip()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "Exit"
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.collidepoint(pygame.mouse.get_pos()):
                            return button.name