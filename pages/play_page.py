import pygame
from pygame import QUIT

from .components.game import Game
from .components.button import Button
from .components.font import Font
from .components.color import Color

class PlayPage:
    def __init__(self, screen):
        self.screen = screen
        self.game = None
        self.initializeImages()
        self.initializeButtons()

    def newGame(self, players):
        self.game = Game(self.screen, players)

    def initializeImages(self):
        self.backgroundImage = pygame.image.load("images/GameBackground.png")

    def initializeButtons(self):
        self.mainPageButton = Button(self.screen, (445, 7, 132, 44), Color.RED, Color.BLACK, Font.make("Garamond", 30), "Main Page", "Main")

    def show(self):
        self.screen.blit(self.backgroundImage, (0, 0))
        self.game.show()
        self.mainPageButton.show()

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "Exit"

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mainPageButton.collidepoint(pygame.mouse.get_pos()):
                        return self.mainPageButton.name
                    
                    if not self.game.isEnded() and self.game.play(event):
                        self.show()