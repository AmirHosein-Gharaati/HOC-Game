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

        self.lines = ["The goal of the game is that you reach the sum of 15 with 3",
                      "cards in your hand. The first person to reach this goal in",
                      "maximum of 30 turns is the winner.",
                      "",
                      "Each time at your turn, you are supposed to take one card",
                      "from the desk.",
                      "When you have 3 cards in your hand, you should swap one",
                      "of your cards in your hand with a card on the desk.",
                      "",
                      "If you have any questions, feel free to ask your supervisor."]
    
    def initializeButtons(self):
        self.mainPageButton = Button(self.screen, (445, 512, 132, 44), Color.RED, Color.BLACK, Font.make("Garamond", 30), "Main Page", "Main")
    
    def initializeImages(self):
        self.mainBackgroundImage = pygame.image.load("images/backgrounds/MainBackground.png")

    def show(self):
        self.screen.blit(self.mainBackgroundImage, (0, 0))
        self.screen.blit(Font.make("Algerian", 116).render("FIFTEEN", 1, Color.BLACK), (290, 0))
        for index, line in enumerate(self.lines):
            self.screen.blit(Font.make("GaramondBold", 28).render(line, 1, Color.BLACK), (160, 140 + index * 34))
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