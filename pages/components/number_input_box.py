import pygame
from .color import Color
from .font import Font

class NumberInputBox:
    def __init__(self, screen, start, startNumber, numberRange, enable=True):
        self.screen = screen

        self.numberFont = pygame.font.Font(None, 32)
        self.signsFont = pygame.font.Font(None, 40)

        self.startX, self.startY = start
        self.height = self.numberFont.render("00", True, Color.BLACK).get_rect().height + 10
        self.width = self.numberFont.render("00", True, Color.BLACK).get_rect().height + 30

        self.number = startNumber
        self.minimumNumber, self.maximumNumber = numberRange

        self.enable = enable
        self.area = None

    def isDisable(self):    return not self.enable
    def isEnable(self):     return self.enable
    def setEnable(self):    self.enable = True
    def setDisable(self):   self.enable = False

    def increase(self):
        self.number = min(self.number + 1, self.maximumNumber)
    def decrease(self):
        self.number = max(self.number - 1, self.minimumNumber)

    def show(self):
        self.area = pygame.draw.rect(self.screen, Color.BLACK, (self.startX - 3 - self.height, self.startY - 3, self.width + 6 + 2 * self.height, self.height + 6))
        pygame.draw.rect(self.screen, Color.WHITE, (self.startX, self.startY, self.width, self.height))

        self.decreamentArea = pygame.draw.rect(self.screen, Color.RED if self.isEnable() else Color.GRAY52, (self.startX - self.height, self.startY, self.height, self.height))
        self.increamentArea = pygame.draw.rect(self.screen, Color.BLUE if self.isEnable() else Color.GRAY52, (self.startX + self.width, self.startY, self.height, self.height))

        self.screen.blit(self.signsFont.render("-", 1, Color.BLACK), (self.startX - 20, self.startY + 3))
        self.screen.blit(self.signsFont.render("+", 1, Color.BLACK), (self.startX + self.width + 9, self.startY + 2))

        numberText = self.numberFont.render(str(self.number), 1, Color.BLACK)
        self.screen.blit(numberText, numberText.get_rect(midtop=(self.startX + self.width / 2, self.startY + 5)))

        pygame.display.flip()

    def collidepoint(self, position):
        return self.area.collidepoint(position)

    def update(self, event):
        if self.isEnable() and event.type == pygame.MOUSEBUTTONDOWN:
            if (self.increamentArea.collidepoint(pygame.mouse.get_pos()) and event.button == 1) or (self.collidepoint(pygame.mouse.get_pos()) and event.button == 4):
                self.increase()
                self.show()

            elif (self.decreamentArea.collidepoint(pygame.mouse.get_pos()) and event.button == 1) or (self.collidepoint(pygame.mouse.get_pos()) and event.button == 5):
                self.decrease()
                self.show()