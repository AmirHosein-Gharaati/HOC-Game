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

    def newGame(self, players):
        self.game = Game(self.screen, players)

    def initializeImages(self):
        self.backgroundImage = pygame.image.load("images/GameBackground.png")

    def initializeButtons(self):
        self.mainPageButton = Button(self.screen, [445, 7, 132, 44], Color.RED, Color.BLACK, Font.make("Garamond", 30), "Main Page", "Main")

    def show(self):
        if not self.game.noHuman():
            self.screen.blit(self.backgroundImage, (0, 0))
            self.game.show()
            self.mainPageButton.show()
        else:
            self.game.show()

        pygame.display.flip()

    def logThread(self):
        starttime = time.time()
        while not self.game.isEnded():
            self.game.agentPlay()
            self.game.nextTurn()
            self.show()
            time.sleep(1.0 - ((time.time() - starttime) % 1.0))

        self.game.textBox.add(" ", "lightgray")
        self.game.textBox.add(" Enter any key to back to the main menu ... ", "gray")
        self.show()

    def run(self):
        if self.game.noHuman():
            self.game.textBox.add("  --- game started ---   ", "blue")
            self.show()
            time.sleep(1.0)
            t = Thread(target=self.logThread)
            t.daemon = True
            t.start()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "Exit"

                elif not self.game.noHuman() and event.type == pygame.MOUSEBUTTONDOWN and self.mainPageButton.collidepoint(pygame.mouse.get_pos()):
                    return self.mainPageButton.name

                elif self.game.noHuman() and self.game.isEnded() and event.type == pygame.KEYDOWN:
                    return self.mainPageButton.name
                    
                elif self.game.play(event):
                    self.show()