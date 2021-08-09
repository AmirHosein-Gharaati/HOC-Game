import pygame

from .color import Color

class SwitchBox:
    def __init__(self, screen, startX, startY, options, font, textColor, circleRadius, selected=0):
        self.screen = screen
        self.startX = startX
        self.startY = startY
        self.options = options
        self.selected = selected
        self.font = font
        self.textColor = textColor

        self.circleRadius = circleRadius
        self.border = 2
        self.width = self.circleRadius * 4 + self.border * 2
        self.height = self.circleRadius * 2 + self.border * 2

    def show(self):
        self.area = pygame.draw.rect(self.screen, Color.BLACK, (self.startX - self.border, self.startY - self.border, self.width + self.border * 2, self.height + self.border * 2), border_radius=17)
        pygame.draw.rect(self.screen, Color.WHITE, (self.startX, self.startY, self.width, self.height), border_radius=15)
        pygame.draw.circle(self.screen, Color.RED, (self.startX + 2 + self.selected * self.circleRadius * 2 + self.circleRadius, self.startY + 2 + self.circleRadius), self.circleRadius)

        text = self.font.render(self.options[0], 1, self.textColor)
        self.screen.blit(text, text.get_rect(midright=(self.startX - 7, self.startY + 2 + self.circleRadius - 3)))

        text = self.font.render(self.options[1], 1, self.textColor)
        self.screen.blit(text, text.get_rect(midleft=(self.startX + self.width + 7, self.startY + 2 + self.circleRadius - 3)))

    def getSelected(self):
        return self.options[self.selected]

    def reverseSelected(self):
        self.selected ^= 1

    def collidepoint(self, position):
        return self.area.collidepoint(position)