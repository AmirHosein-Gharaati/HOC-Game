import pygame
import clipboard
from .color import Color


class InputBox:
    @staticmethod
    def isValidCharacter(character):
        return "a" <= character.lower() <= "z" or "0" <= character <= "9" or character in ("_", "-", "/", ".")

    def __init__(self, screen, startX, startY, width, defaultText="", allow_double_line=False):
        self.startX = startX
        self.startY = startY
        self.active = False
        self.enable = True

        self.area = None
        self.screen = screen

        self.defaultFont = pygame.font.Font(None, 32)
        self.width = width
        self.allow_double_line = allow_double_line
        self.height = self.defaultFont.render("W"*15, True, Color.BLACK).get_rect().height + 10
        if self.allow_double_line:
            self.line2StartY = self.startY + self.height - 5
            self.height = self.height * 2 - 5
            self.textLine2 = ""

        self.setText(defaultText)

    def isActive(self):     return self.active
    def setActive(self):    self.active = True
    def setInActive(self):  self.active = False

    def isDisable(self):    return not self.enable
    def setEnable(self):    self.enable = True
    def setDisable(self):   self.enable = False; self.active = False

    def addText(self, character):
        if InputBox.isValidCharacter(character):
            if self.defaultFont.render(self.text + character, True, Color.BLACK).get_rect().width + 5 < self.width:
                self.text += character
            elif self.allow_double_line and self.defaultFont.render(self.textLine2 + character, True, Color.BLACK).get_rect().width + 5 < self.width:
                self.textLine2 += character

    def setText(self, string):
        if all(InputBox.isValidCharacter(character) for character in string):
            if not self.allow_double_line:
                if self.defaultFont.render(string, True, Color.BLACK).get_rect().width < self.width:
                    self.text = string
            else:
                line2String = ""
                while self.defaultFont.render(string, True, Color.BLACK).get_rect().width >= self.width:
                    line2String = string[-1] + line2String
                    string = string[:-1]
                if self.defaultFont.render(line2String, True, Color.BLACK).get_rect().width < self.width:
                    self.text = string
                    self.textLine2 = line2String

    def getText(self):
        return self.text + (self.textLine2 if self.allow_double_line else "")

    def cleanText(self):
        self.text = ""
        if self.allow_double_line:
            self.textLine2 = ""

    def removeLastOfText(self):
        if self.allow_double_line and self.textLine2 != "":
            self.textLine2 = self.textLine2[:-1]
        else:
            self.text = self.text[:-1]

    def show(self):
        self.area = pygame.draw.rect(self.screen,
                                     Color.RED if self.active else Color.BLACK,
                                     (self.startX - 3, self.startY - 3, self.width + 6, self.height + 6))
        pygame.draw.rect(self.screen,
                         Color.WHITE,
                         (self.startX, self.startY, self.width, self.height))
        text = self.defaultFont.render(self.text, True, Color.BLACK)
        self.screen.blit(text, text.get_rect(topleft=(self.startX + 5, self.startY + 5)))

        if self.allow_double_line:
            textLine2 = self.defaultFont.render(self.textLine2, True, Color.BLACK)
            self.screen.blit(textLine2, textLine2.get_rect(topleft=(self.startX + 5, self.line2StartY + 5)))

        if self.isDisable():
            shadow = pygame.Surface((self.width + 6, self.height + 6), pygame.SRCALPHA)
            shadow.fill((*Color.BLACK, 100))
            self.screen.blit(shadow, (self.startX - 3, self.startY - 3))

        pygame.display.flip()

    def collidepoint(self, position):
        return self.area.collidepoint(position)

    def update(self, event):
        if not self.isDisable():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.setActive() if self.collidepoint(pygame.mouse.get_pos()) else self.setInActive()

            elif event.type == pygame.KEYDOWN and self.isActive():
                if event.key == pygame.K_BACKSPACE:
                    self.removeLastOfText()
                elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if event.key == pygame.K_v:
                        self.setText(clipboard.paste())
                    elif event.key == pygame.K_c:
                        clipboard.copy(self.getText())
                    elif event.key == pygame.K_x:
                        clipboard.copy(self.getText())
                        self.cleanText()
                elif event.key in (pygame.K_ESCAPE, pygame.K_DELETE):
                    self.cleanText()
                else:
                    self.addText(event.unicode)

        self.show()
