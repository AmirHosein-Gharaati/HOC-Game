import pygame
from pygame import QUIT

from threading import Thread
import time

from .components.game import Game
from .components.button import Button
from .components.font import Font
from .components.color import Color
from .components.switch_box import SwitchBox

class PlayPage:
    def __init__(self, screen):
        self.screen = screen
        self.game = None
        self.initializeImages()
        self.initializeButtons()

    def newGame(self, players):
        self.agentVSagentPageModeButton = SwitchBox(self.screen, 480, 650, ("Board", "Console"), Font.make("Garamond", 25), Color.BLACK, 8)
        self.game = Game(self.screen, players, 1.0, 0, self.agentVSagentPageModeButton.getSelected())

    def initializeImages(self):
        self.logBackgroundImage = pygame.image.load("images/backgrounds/LogsPageBackground.png")
        self.logBackgroundUpImage = pygame.image.load("images/backgrounds/LogsPageBackgroundUp.png")
        self.logBackgroundDownImage = pygame.image.load("images/backgrounds/LogsPageBackgroundDown.png")

        self.backgroundImage = pygame.image.load("images/backgrounds/GameBackground.png")

    def initializeButtons(self):
        self.mainPageButton = Button(self.screen, [445, 7, 132, 44], Color.RED, Color.BLACK, Font.make("Garamond", 30), "Main Page", "Main")

    def show(self):
        if self.game.noHuman() and self.game.agentVSagentPageMode == "Console":
            self.screen.blit(self.logBackgroundImage, (0, 0))
            self.game.show()
            self.screen.blit(self.logBackgroundUpImage, (0, 0))
            self.screen.blit(self.logBackgroundDownImage, (0, 600))

        else:
            self.screen.blit(self.backgroundImage, (0, 0))
            self.game.show()

        if self.game.noHuman():
            self.agentVSagentPageModeButton.show()

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
        if self.game.noHuman() :
            self.game.textBox.add("  $  Game Started  $", Color.DEEPSKYBLUE2, center=True)
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

                elif event.type == pygame.MOUSEBUTTONDOWN and self.game.noHuman() and self.agentVSagentPageModeButton.collidepoint(pygame.mouse.get_pos()):
                    self.agentVSagentPageModeButton.reverseSelected()
                    self.game.agentVSagentPageMode = self.agentVSagentPageModeButton.getSelected()
                    self.show()

                elif self.game.play(event):
                    self.show()