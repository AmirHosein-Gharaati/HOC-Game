import pygame

from pygame.locals import QUIT

from .components.button import Button
from .components.color import Color

class MainPage:
    def __init__(self, screen):
        self.screen = screen
        self.initializeImages()
        self.initializeFonts()
        self.initializeButtons()
    
    def initializeButtons(self):
        self.buttons = [
            Button((321, 320, 380, 70), Color.RED, self.Garamond45Font, self.screen, "Play"),
            Button((321, 420, 380, 70), Color.BLUE, self.Garamond45Font, self.screen, "Help")
        ]
    
    def initializeImages(self):
        self.mainBackgroundImage = pygame.image.load("images/MainBackground.png")
        self.card15Image = pygame.image.load("images/cards/15.png")
    
    def initializeFonts(self):
        self.Garamond45Font = pygame.font.Font("fonts/EBGaramond-VariableFont_wght.ttf", 40)
        self.Algerian116Font = pygame.font.Font("fonts/Algerian Regular.ttf", 116)

    
    def show(self):
        self.screen.blit(self.mainBackgroundImage, (0, 0))
        self.screen.blit(self.Algerian116Font.render("FIFTEEN", 1, Color.BLACK), (290, 0))
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