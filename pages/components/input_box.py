import pygame
import clipboard
from .color import Color


class InputBox:
    @staticmethod
    def isValidCharacter(character):
        return "a" <= character.lower() <= "z" or "1" <= character <= "9" or character in ("_", "-", "/", ".")

    def __init__(self, screen, startX, startY, width, defaultText=""):
        self.text = defaultText
        self.startX = startX
        self.startY = startY
        self.active = False
        self.enable = True

        self.area = None
        self.screen = screen

        self.defaultFont = pygame.font.Font(None, 32)
        self.width = width
        self.height = self.defaultFont.render("W"*15, True, Color.BLACK).get_rect().height + 10

    def isActive(self):     return self.active
    def setActive(self):    self.active = True
    def setInActive(self):  self.active = False

    def isDisable(self):    return not self.enable
    def setEnable(self):    self.enable = True
    def setDisable(self):   self.enable = False; self.active = False

    def addText(self, character):
        if self.defaultFont.render(self.text+character, True, Color.BLACK).get_rect().width + 5 < self.width and InputBox.isValidCharacter(character):
            self.text += character

    def setText(self, string):
        if self.defaultFont.render(string, True, Color.BLACK).get_rect().width < self.width and all(InputBox.isValidCharacter(character) for character in string):
            self.text = string

    def removeLastOfText(self):
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
                        clipboard.copy(self.text)
                    elif event.key == pygame.K_x:
                        clipboard.copy(self.text)
                        self.text = ""
                elif event.key in (pygame.K_ESCAPE, pygame.K_DELETE):
                    self.text = ""
                else:
                    self.addText(event.unicode)

        self.show()
