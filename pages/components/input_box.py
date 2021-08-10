import pygame
import clipboard
from .color import Color


class InputBox:
    @staticmethod
    def isValidCharacter(character):
        return "a" <= character.lower() <= "z" or "0" <= character <= "9" or character in ("_", "-", "/", ".")

    def __init__(self, screen, startX, startY, width, defaultText=""):
        self.startX = startX
        self.startY = startY
        self.active = False
        self.enable = True

        self.area = None
        self.screen = screen

        self.cursorIndex = len(defaultText)

        self.defaultFont = pygame.font.Font(None, 32)
        self.width = width
        self.height = self.defaultFont.render("W"*15, True, Color.BLACK).get_rect().height + 10

        self.setText(defaultText)

        self.blink = 0

    def isActive(self):     return self.active
    def setActive(self):    self.active = True; self.cursorIndex = len(self.text)
    def setInActive(self):  self.active = False

    def isDisable(self):    return not self.enable
    def setEnable(self):    self.enable = True
    def setDisable(self):   self.enable = False; self.active = False

    def addText(self, character):
        if InputBox.isValidCharacter(character):
            if self.defaultFont.render(self.text + character, True, Color.BLACK).get_rect().width + 5 < self.width:
                self.text = self.text[:self.cursorIndex] + character + self.text[self.cursorIndex:]
                self.cursorIndex += 1

    def setText(self, string):
        self.cursorIndex = len(string)
        if all(InputBox.isValidCharacter(character) for character in string):
            if self.defaultFont.render(string, True, Color.BLACK).get_rect().width < self.width:
                self.text = string

    def getText(self):
        return self.text

    def cleanText(self):
        self.cursorIndex = 0
        self.text = ""

    def removeFromText(self):
        self.text = self.text[:self.cursorIndex-1] + self.text[self.cursorIndex:]
        self.cursorIndex = max(self.cursorIndex - 1, 0)

    def show(self):
        self.area = pygame.draw.rect(self.screen,
                                     Color.RED if self.active else Color.BLACK,
                                     (self.startX - 3, self.startY - 3, self.width + 6, self.height + 6))
        pygame.draw.rect(self.screen,
                         Color.WHITE,
                         (self.startX, self.startY, self.width, self.height))
        extraCharacter = ("" if not self.active else ("|" if self.blink // 90 else " "))
        textWithCursor = self.text[:self.cursorIndex] + extraCharacter + self.text[self.cursorIndex:]
        self.blink = (self.blink + 1) % 180
        text = self.defaultFont.render(textWithCursor, True, Color.BLACK)
        self.screen.blit(text, text.get_rect(topleft=(self.startX + 5, self.startY + 5)))

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
                    self.removeFromText()
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
                elif event.key == pygame.K_LEFT:
                    self.cursorIndex = max(self.cursorIndex - 1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.cursorIndex = min(self.cursorIndex + 1, len(self.text))
                elif event.key == pygame.K_HOME:
                    self.cursorIndex = 0
                elif event.key == pygame.K_END:
                    self.cursorIndex = len(self.text)
                else:
                    self.addText(event.unicode)

        self.show()