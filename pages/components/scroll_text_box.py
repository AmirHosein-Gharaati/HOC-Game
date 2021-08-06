import pygame


class ScrollTextBox:
    def __init__(self, screen, font, startX, startY):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        self.font = font

        self.lines = []
        self.startX = startX
        self.startY = startY
        self.lineSpacing = self.font.get_height() + 15

        self.scrollY = 0

        self.intermediate = pygame.surface.Surface((self.width, self.height))

    def getEndY(self):
        return self.startY + self.lineSpacing * (len(self.lines))

    def increaseHeight(self):
        self.height += self.lineSpacing
        self.intermediate = pygame.surface.Surface((self.width, self.height))
        for lineIndex, line in enumerate(self.lines):
            self.intermediate.blit(self.font.render(line["text"], True, line["color"]),
                                   (self.startX, self.startY + self.lineSpacing * lineIndex))

    def add(self, text, color):
        lineY = self.startY + self.lineSpacing * (len(self.lines))
        if lineY + self.lineSpacing > self.intermediate.get_height():
            self.increaseHeight()

        self.intermediate.blit(self.font.render(text, True, color), (self.startX, lineY))
        self.lines.append({"text": text, "color": color})

        self.scrollY = self.screen.get_height() - self.height

    def show(self):
        self.screen.blit(self.intermediate, (0, self.scrollY))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5):
            if event.button == 4:
                self.scrollY = min(self.scrollY + 15, 0)
            else:
                self.scrollY = max(self.scrollY - 15, self.screen.get_height() - self.height)
