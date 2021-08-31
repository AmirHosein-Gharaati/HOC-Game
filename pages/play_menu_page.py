import pygame
from pygame.locals import QUIT

import os.path

from .components.player import Player
from .components.button import Button
from .components.radio_button import RadioButton
from .components.color import Color
from .components.input_box import InputBox
from .components.number_input_box import NumberInputBox
from .components.switch_box import SwitchBox
from .components.font import Font

class PlayMenuPage:
    def __init__(self, screen):
        self.screen = screen
        self.initializeImages()

        self.player1FilePath = self.player2FilePath = ""
        self.player1FileIsValid = self.player2FileIsValid = False
        self.initializeButtons()
        
    def initializeButtons(self):
        self.mainPageButton = Button(self.screen, (370, 625, 142, 44), Color.RED, Color.BLACK, Font.make("Garamond", 30), "Main Page", "Main")
        self.startPageButton = Button(self.screen, (530, 625, 122, 44), Color.GREEN, Color.BLACK, Font.make("Garamond", 30), "Start")

        self.player1ModeButton = RadioButton(self.screen, ("Human", "Agent"), 300, 160)
        self.player2ModeButton = RadioButton(self.screen, ("Human", "Agent"), 690, 160, False)

        self.player1NameBox = InputBox(self.screen, 160, 300, 295, "Player1")
        self.player2NameBox = InputBox(self.screen, 565, 300, 295, "Player2")

        self.player1FileOpenButton = Button(self.screen, (340, 390, 100, 50), Color.ORANGE, Color.BLACK, Font.make("Garamond", 30), "Drop", enable=False)
        self.player2FileOpenButton = Button(self.screen, (580, 390, 100, 50), Color.ORANGE, Color.BLACK, Font.make("Garamond", 30), "Drop", enable=False)

        self.agentVsAgentModeButton = SwitchBox(self.screen, 360, 500, ("Show Game", "Just Results"), Font.make("Garamond", 25), Color.BLACK, 8)
        self.numberOfRoundsBox = NumberInputBox(self.screen, (630, 510), 1, (1, 10), enable=False)

    def initializeImages(self):
        self.mainBackgroundImage = pygame.image.load("images/backgrounds/MainBackground.png")
        self.tickImage = pygame.image.load("images/tick.png")
        self.crossImage = pygame.image.load("images/cross.png")

    def isBothAgent(self):
        return self.player1ModeButton.selected() == "Agent" and self.player2ModeButton.selected() == "Agent"

    def extractFileName(self, filePath: str):
        fileName = filePath[filePath.rfind("/")+1:].rstrip(".py")
        return fileName

    def show(self):
        self.screen.blit(self.mainBackgroundImage, (0, 0))
        self.screen.blit(Font.make("Algerian", 116).render("FIFTEEN", 1, Color.BLACK), (290, 0))
        
        self.mainPageButton.show()
        self.startPageButton.show()

        self.player1ModeButton.show()
        self.player2ModeButton.show()

        self.screen.blit(Font.make("Garamond", 25).render("Name", 1, Color.BLACK), (480, 297))
        self.player1NameBox.show()
        self.player2NameBox.show()

        self.screen.blit(Font.make("Garamond", 25).render("Code File", 1, Color.BLACK), (463, 397))
        self.player1FileOpenButton.show()
        self.player2FileOpenButton.show()

        if self.isBothAgent():
            self.screen.blit(Font.make("Garamond", 20).render("Number of Rounds", 1, Color.BLACK), (580, 480))
            self.agentVsAgentModeButton.show()
            self.numberOfRoundsBox.show()

        if not self.player1FileOpenButton.isDisable():
            self.screen.blit(self.tickImage if self.player1FileIsValid else self.crossImage, (298, 408))
            fileName = self.extractFileName(self.player1FilePath)
            text = Font.make("Garamond", 20).render(fileName, 1, Color.BLACK)
            if text.get_width() > 132:
                while text.get_width() > 132:
                    fileName = fileName[:-1]
                    text = Font.make("Garamond", 20).render(fileName + "...", 1, Color.BLACK)
            self.screen.blit(text, text.get_rect(topright=(293, 410)))

        if not self.player2FileOpenButton.isDisable():
            self.screen.blit(self.tickImage if self.player2FileIsValid else self.crossImage, (688, 408))
            fileName = self.extractFileName(self.player2FilePath)
            text = Font.make("Garamond", 20).render(fileName, 1, Color.BLACK)
            if text.get_width() > 132:
                while text.get_width() > 132:
                    fileName = fileName[:-1]
                    text = Font.make("Garamond", 20).render(fileName + "...", 1, Color.BLACK)
            self.screen.blit(text, text.get_rect(topleft=(730, 410)))

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "Exit", None, None
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mainPageButton.collidepoint(pygame.mouse.get_pos()):
                        return self.mainPageButton.name, None, None
                    
                    elif self.startPageButton.collidepoint(pygame.mouse.get_pos()):
                        if (self.player1FileOpenButton.isDisable() or self.player1FileIsValid) and (self.player2FileOpenButton.isDisable() or self.player2FileIsValid):
                            player1 = Player(self.player1NameBox.text, self.player1ModeButton.selected(), self.player1FilePath)
                            player2 = Player(self.player2NameBox.text, self.player2ModeButton.selected(), self.player2FilePath)
                            justResult = self.isBothAgent() and self.agentVsAgentModeButton.getSelected() == "Just Results"
                            return self.startPageButton.name, (player1, player2), (justResult, self.numberOfRoundsBox.number if justResult else 0)
                    
                    elif self.player1ModeButton.collidepoint(pygame.mouse.get_pos()):
                        before = self.player1ModeButton.selected()

                        self.player1ModeButton.update(pygame.mouse.get_pos())
                        if self.player1ModeButton.selected() == "Human":
                            self.player1FileOpenButton.setDisable()
                        else:
                            self.player1FileOpenButton.setEnable()

                        if before != self.player1ModeButton.selected():
                            self.show()
                    
                    elif self.player2ModeButton.collidepoint(pygame.mouse.get_pos()):
                        before = self.player2ModeButton.selected()

                        self.player2ModeButton.update(pygame.mouse.get_pos())
                        if self.player2ModeButton.selected() == "Human":
                            self.player2FileOpenButton.setDisable()
                        else:
                            self.player2FileOpenButton.setEnable()

                        if before != self.player2ModeButton.selected():
                            self.show()

                    elif self.isBothAgent() and self.agentVsAgentModeButton.collidepoint(pygame.mouse.get_pos()):
                        self.agentVsAgentModeButton.reverseSelected()
                        if self.agentVsAgentModeButton.getSelected() == "Just Results":
                            self.numberOfRoundsBox.setEnable()
                        else:
                            self.numberOfRoundsBox.setDisable()
                        self.show()

                elif event.type == pygame.DROPFILE and os.path.splitext(event.file)[-1] == ".py":
                    mousePos = pygame.mouse.get_pos()
                    filePath = event.file.replace("\\", "/")
                    if self.player1FileOpenButton.isEnable() and self.player1FileOpenButton.collidepoint(mousePos):
                        self.player1FilePath = filePath
                        self.player1FileIsValid = Player.isCodeFileValid(self.player1FilePath)
                        self.show()

                    elif self.player2FileOpenButton.isEnable() and self.player2FileOpenButton.collidepoint(mousePos):
                        self.player2FilePath = filePath
                        self.player2FileIsValid = Player.isCodeFileValid(self.player2FilePath)
                        self.show()

                self.numberOfRoundsBox.update(event)
                self.player1NameBox.update(event)
                self.player2NameBox.update(event)

            self.player1NameBox.show()
            self.player2NameBox.show()