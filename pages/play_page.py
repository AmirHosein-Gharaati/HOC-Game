import pygame
from pygame import QUIT

from threading import Thread
import time

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

    def newGame(self, players, agentDelayTime=1.0):
        self.game = Game(self.screen, players, agentDelayTime)

    def initializeImages(self):
        self.logBackgroundImage = pygame.image.load("images/backgrounds/LogsPageBackground.png")
        self.logBackgroundUpImage = pygame.image.load("images/backgrounds/LogsPageBackgroundUp.png")
        self.logBackgroundDownImage = pygame.image.load("images/backgrounds/LogsPageBackgroundDown.png")

        self.backgroundImage = pygame.image.load("images/backgrounds/GameBackground.png")

    def initializeButtons(self):
        self.mainPageButton = Button(self.screen, [445, 7, 132, 44], Color.RED, Color.BLACK, Font.make("Garamond", 30), "Main Page", "Main")

    def show(self):
        if not self.game.noHuman():
            self.screen.blit(self.backgroundImage, (0, 0))
            self.game.show()

        else:
            self.screen.blit(self.logBackgroundImage, (0, 0))
            self.game.show()
            self.screen.blit(self.logBackgroundUpImage, (0, 0))
            self.screen.blit(self.logBackgroundDownImage, (0, 600))

        self.mainPageButton.show()

        pygame.display.flip()

    def logThread(self):
        self.threadContinue = True

        while not self.game.isEnded():
            self.game.agentPlay()
            self.game.nextTurn()
            if not self.threadContinue: break
            self.show()

    def run(self):
        if self.game.noHuman():
            self.game.textBox.add("  $  Game Started  $", Color.DEEPSKYBLUE2)
            self.show()
            t = Thread(target=self.logThread)
            t.daemon = True
            t.start()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "Exit"

                elif event.type == pygame.MOUSEBUTTONDOWN and self.mainPageButton.collidepoint(pygame.mouse.get_pos()):
                    if self.game.noHuman(): self.threadContinue = False
                    return self.mainPageButton.name
                    
                elif self.game.play(event):
                    self.show()