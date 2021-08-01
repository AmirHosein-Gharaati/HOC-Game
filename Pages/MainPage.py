import pygame

from pygame.locals import QUIT

from .Components.Button import Button
from .Components import Color

class MainPage:
    def __init__(self, screen):
        self.screen = screen
        self.initializeImages()
        self.initializeFonts()
        self.initializeButtons()

    
    def show(self):
        self.screen.blit(self.mainBackgroundImage, (0, 0))
        
        self.screen.blit(self.Algerian116Font.render("FIFTEEN", 1, Color.BLACK), (290, 0))
        self.screen.blit(self.card15Image, (423, 121))
        
        for button in self.buttons: button.show()
        
        pygame.display.flip()
    
    def initializeButtons(self):
        gameButtonsName = ("Human vs Human", "Human vs Agent", "Agent vs Agent")
        self.buttons = []
        for buttonIndex, buttonName in enumerate(gameButtonsName):
            gameButton = Button((321, buttonIndex*78+264, 380, 70),
                                Color.GRAY,
                                buttonName,
                                self.Garamond45Font,
                                self.screen)
            self.buttons.append(gameButton)
        
        self.buttons.append(Button((530, 512, 112, 44), Color.RED, "Exit", self.Garamond30Font, self.screen))
        
        self.buttons.append(Button((390, 512, 112, 44), Color.BLUE, "Help", self.Garamond30Font, self.screen))
    
    def initializeImages(self):
        self.mainBackgroundImage = pygame.image.load("images/MainBackground.png")
        self.card15Image = pygame.image.load("images/cards/15.png")
    
    def initializeFonts(self):
        self.Garamond30Font = pygame.font.Font("fonts/EBGaramond-VariableFont_wght.ttf", 30)
        self.Garamond45Font = pygame.font.Font("fonts/EBGaramond-VariableFont_wght.ttf", 40)
        self.Algerian116Font = pygame.font.Font("fonts/Algerian Regular.ttf", 116)
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "Exit"
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.collidepoint(pygame.mouse.get_pos()):
                            return button.name