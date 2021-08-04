import pygame

class Card:
    slectedBorderImage = pygame.image.load("images/cards/selectedBorder.png")

    def __init__(self, screen, number):
        self.screen = screen
        self.number = number
        self.selected = False
        self.statusOnBoard = [0, 0]
        self.initializeImage()

    def initializeImage(self):
        self.image = pygame.image.load(f"images/cards/{self.number}.png")

    def setSelected(self):      self.selected = True
    def setUnSelected(self):    self.selected = False
    def isSelected(self):       return self.selected

    def __int__(self):
        return self.number

    def startCoordinates(self):
        if self.statusOnBoard[0] == 0:
            startX = 270 + 131 * ((self.number - 1) % 4)
            startY = (208, 373)[(self.number - 1) // 4]

        else:
            startX = (65, 866)[self.statusOnBoard[0] - 1]
            startY = 292 + self.statusOnBoard[1] * 132

        return (startX, startY)

    def show(self):
        startCoor = self.startCoordinates()

        if self.isSelected():
            self.screen.blit(Card.slectedBorderImage, Card.slectedBorderImage.get_rect(topleft=[coor - 3 for coor in startCoor]))

        self.screen.blit(self.image, startCoor)

    def collidepoint(self, position):
        return self.image.get_rect(topleft=self.startCoordinates()).collidepoint(position)