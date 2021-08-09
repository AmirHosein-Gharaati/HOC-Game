import pygame
from .color import Color


class Button:
    def __init__(self, screen, sizes, color, textColor, font, text, name=None, enable=True):
        self.sizes = sizes
        self.color = color
        self.disableColor = Color.GRAY69
        self.textColor = textColor
        self.text = text
        self.name = name or text
        self.font = font
        self.area = None
        self.screen = screen
        self.enable = enable

    def isDisable(self):    return not self.enable
    def setEnable(self):    self.enable = True
    def setDisable(self):   self.enable = False

    def show(self):
        border = pygame.draw.rect(self.screen,
                                  Color.BLACK,
                                  [self.sizes[0] - 3, self.sizes[1] - 3,
                                   self.sizes[2] + 6, self.sizes[3] + 6],
                                  border_radius=6)
        pygame.draw.rect(self.screen, (self.color if not self.isDisable() else self.disableColor), self.sizes, border_radius=4)

        text = self.font.render(self.text, 1, self.textColor)
        textRect = text.get_rect(center=(self.sizes[0] + self.sizes[2] / 2,
                                         self.sizes[1] + self.sizes[3] / 2 - 3))
        self.screen.blit(text, textRect)

        self.area = border

    def collidepoint(self, position):
        return self.area.collidepoint(position)
