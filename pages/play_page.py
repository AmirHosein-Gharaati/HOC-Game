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

    def newGame(self, players, agentVsAgentMore):
        self.agentVsAgentJustResult, self.agentVsAgentNumberOfRounds = agentVsAgentMore
        if self.agentVsAgentJustResult:
            self.result = {players[0]: 0, players[1]: 0, None: 0}
        delayTime = 0.0 if self.agentVsAgentJustResult else 1.0

        self.agentVSagentPageModeButton = SwitchBox(self.screen, 480, 650, ("Board", "Console"), Font.make("Garamond", 25), Color.BLACK, 8)
        self.game = Game(self.screen, players, delayTime, 0, self.agentVSagentPageModeButton.getSelected())

    def initializeImages(self):
        self.logBackgroundImage = pygame.image.load("images/backgrounds/LogsPageBackground.png")
        self.logBackgroundUpImage = pygame.image.load("images/backgrounds/LogsPageBackgroundUp.png")
        self.logBackgroundDownImage = pygame.image.load("images/backgrounds/LogsPageBackgroundDown.png")

        self.backgroundImage = pygame.image.load("images/backgrounds/GameBackground.png")

    def initializeButtons(self):
        self.mainPageButton = Button(self.screen, [445, 7, 132, 44], Color.RED, Color.BLACK, Font.make("Garamond", 30), "Main Page", "Main")
        self.rematchPageButton = Button(self.screen, [519, 7, 132, 44], Color.RED, Color.BLACK, Font.make("Garamond", 30), "Rematch", "Start")

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

        if self.game.isEnded():
            self.mainPageButton.show(371)
            self.rematchPageButton.show()
        else:
            self.mainPageButton.show()

        pygame.display.flip()

    def logThread(self):
        self.threadContinue = True

        while not self.game.isEnded():
            self.game.agentPlay()
            self.game.nextTurn()
            if not self.threadContinue: break
            self.show()

    def justResultPlayShow(self, showButtons):
        self.screen.blit(self.backgroundImage, (0, 0))

        self.screen.blit(Font.make("Garamond", 50).render(f"{self.game.players[0].name}: {self.result[self.game.players[0]]}", 1, Color.BLACK), (290, 215))
        self.screen.blit(Font.make("Garamond", 50).render(f"{self.game.players[1].name}: {self.result[self.game.players[1]]}", 1, Color.BLACK), (290, 315))
        self.screen.blit(Font.make("Garamond", 50).render(f"Tie: {self.result[None]}", 1, Color.BLACK), (290, 415))

        if showButtons:
            self.mainPageButton.show(371)
            self.rematchPageButton.show()

        pygame.display.flip()

    def justResultPlay(self):
        for round in range(self.agentVsAgentNumberOfRounds):
            self.justResultPlayShow(False)
            while not self.game.isEnded():
                self.game.agentPlay()
                self.game.nextTurn()

            self.result[self.game.getWinner()] += 1
            self.game.reset()

        self.justResultPlayShow(True)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "Exit", None, None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mainPageButton.collidepoint(pygame.mouse.get_pos()):
                        return self.mainPageButton.name, None, None

                    elif self.rematchPageButton.collidepoint(pygame.mouse.get_pos()):
                        return "Start", self.game.players, (self.agentVsAgentJustResult, self.agentVsAgentNumberOfRounds)

    def run(self):
        if self.game.noHuman():
            if self.agentVsAgentJustResult:
                return self.justResultPlay()

            else:
                self.game.textBox.add("  $  Game Started  $", Color.DEEPSKYBLUE2, center=True)
                self.show()
                t = Thread(target=self.logThread)
                t.daemon = True
                t.start()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "Exit", None, None

                elif event.type == pygame.MOUSEBUTTONDOWN and self.mainPageButton.collidepoint(pygame.mouse.get_pos()):
                    if self.game.noHuman(): self.threadContinue = False
                    return self.mainPageButton.name, None, None

                elif event.type == pygame.MOUSEBUTTONDOWN and self.game.noHuman() and self.agentVSagentPageModeButton.collidepoint(pygame.mouse.get_pos()):
                    self.agentVSagentPageModeButton.reverseSelected()
                    self.game.agentVSagentPageMode = self.agentVSagentPageModeButton.getSelected()
                    self.show()

                elif self.game.play(event):
                    self.show()

                if self.game.isEnded() and event.type == pygame.MOUSEBUTTONDOWN and self.rematchPageButton.collidepoint(pygame.mouse.get_pos()):
                    return "Start", self.game.players, (self.agentVsAgentJustResult, self.agentVsAgentNumberOfRounds)