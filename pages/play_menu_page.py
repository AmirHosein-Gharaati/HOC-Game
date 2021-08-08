import pygame
from pygame.locals import QUIT

import tkinter
import tkinter.filedialog

from .components.player import Player
from .components.button import Button
from .components.radio_button import RadioButton
from .components.color import Color
from .components.input_box import InputBox
from .components.font import Font

class PlayMenuPage:
    def __init__(self, screen):
        self.screen = screen
        self.initializeImages()

        self.player1FilePath = self.player2FilePath = ""
        
    def initializeButtons(self):
        self.mainPageButton = Button(self.screen, (370, 500, 142, 44), Color.RED, Color.BLACK, Font.make("Garamond", 30), "Main Page", "Main")
        self.startPageButton = Button(self.screen, (530, 500, 122, 44), Color.GREEN, Color.BLACK, Font.make("Garamond", 30), "Start")

        self.player1ModeButton = RadioButton(self.screen, ("Human", "Agent"), 300, 160)
        self.player2ModeButton = RadioButton(self.screen, ("Human", "Agent"), 690, 160, False)

        self.player1NameBox = InputBox(self.screen, 160, 300, 295, "Player1")
        self.player2NameBox = InputBox(self.screen, 565, 300, 295, "Player2")

        self.player1FileOpenButton = Button(self.screen, (340, 390, 100, 50), "lightseagreen", Color.BLACK, Font.make("Garamond", 30), "Open", enable=False)
        self.player2FileOpenButton = Button(self.screen, (580, 390, 100, 50), "lightseagreen", Color.BLACK, Font.make("Garamond", 30), "Open", enable=False)

    def initializeImages(self):
        self.mainBackgroundImage = pygame.image.load("images/MainBackground.png")

    def prompt_file(self, playerIndex):
        top = tkinter.Tk()
        top.withdraw()
        file_name = tkinter.filedialog.askopenfilename(parent=top, title=f"Player {playerIndex} File", filetypes=[("Python files", "*.py")])
        top.destroy()
        return file_name

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

        self.screen.blit(Font.make("Garamond", 25).render("File Path", 1, Color.BLACK), (466, 397))
        self.player1FileOpenButton.show()
        self.player2FileOpenButton.show()

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "Exit", None
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mainPageButton.collidepoint(pygame.mouse.get_pos()):
                        return self.mainPageButton.name, None
                    
                    if self.startPageButton.collidepoint(pygame.mouse.get_pos()):
                        if (self.player1FileOpenButton.isDisable() or Player.isCodeFileValid(self.player1FilePath)) and (self.player2FileOpenButton.isDisable() or Player.isCodeFileValid(self.player2FilePath)):
                            player1 = Player(self.player1NameBox.text, self.player1ModeButton.selected(), self.player1FilePath)
                            player2 = Player(self.player2NameBox.text, self.player2ModeButton.selected(), self.player2FilePath)
                            return self.startPageButton.name, (player1, player2)
                    
                    elif self.player1ModeButton.collidepoint(pygame.mouse.get_pos()):
                        self.player1ModeButton.update(pygame.mouse.get_pos())
                        if self.player1ModeButton.selected() == "Human":
                            self.player1FileOpenButton.setDisable()
                        else:
                            self.player1FileOpenButton.setEnable()
                        self.player1FileOpenButton.show()
                    
                    elif self.player2ModeButton.collidepoint(pygame.mouse.get_pos()):
                        self.player2ModeButton.update(pygame.mouse.get_pos())
                        if self.player2ModeButton.selected() == "Human":
                            self.player2FileOpenButton.setDisable()
                        else:
                            self.player2FileOpenButton.setEnable()
                        self.player2FileOpenButton.show()

                    elif not self.player1FileOpenButton.isDisable() and self.player1FileOpenButton.collidepoint(pygame.mouse.get_pos()):
                        self.player1FilePath = self.prompt_file(1)

                    elif not self.player2FileOpenButton.isDisable() and self.player2FileOpenButton.collidepoint(pygame.mouse.get_pos()):
                        self.player2FilePath = self.prompt_file(2)

                self.player1NameBox.update(event)
                self.player2NameBox.update(event)