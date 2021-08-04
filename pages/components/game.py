import pygame

from .card import Card
from .color import Color
from .font import Font

class Game:
    playerMaxTurn = 30

    def __init__(self, screen, players):
        self.screen = screen
        self.players = players
        self.cards = [Card(screen, cardNumber) for cardNumber in range(1, 9)]
        self.playedTurns = [0, 0]
        self.selectedCard = None
        self.turn = 0
        self.ended = False

        self.initializeImage()

    def initializeImage(self):
        self.shieldsTurnImage = pygame.image.load("images/ShieldTurn.png")
        self.shieldsOtherImage = pygame.image.load("images/ShieldOther.png")
        self.shieldsImageStartX = [21, 822]

    def nextTurn(self):
        self.playedTurns[self.turn] += 1
        self.turn = 1 - self.turn

    def getClickedCard(self, position):
        return next((card for card in self.cards if card.collidepoint(position)), None)

    def getCardsOfPlayer(self, playerIndex):
        return [card for card in self.cards if card.statusOnBoard[0] - 1 == playerIndex]

    def isEnded(self):
        return self.ended

    def getWinner(self):
        for playerIndex in (0, 1):
            turnPlayerCards = self.getCardsOfPlayer(playerIndex)
            if len(turnPlayerCards) == 3 and sum(map(int, turnPlayerCards)) == 15:
                return self.players[playerIndex]
        return None

    def show(self):
        winner = self.getWinner()

        for card in self.cards:
            card.show()

        for playerIndex in (0, 1):
            self.screen.blit(self.shieldsTurnImage if playerIndex == self.turn and winner == None else self.shieldsOtherImage, (self.shieldsImageStartX[playerIndex], 26))

            playerNameFontSize = 25
            while True:
                playerNameText = Font.make("GaramondBold", playerNameFontSize).render(self.players[playerIndex].name, 1, Color.WHITE)
                playerNameTextRect = playerNameText.get_rect()
                if playerNameTextRect.width < 150: break
                playerNameFontSize -= 3
            playerNameTextRect.midtop = (self.shieldsImageStartX[playerIndex]+89, 85)
            self.screen.blit(playerNameText, playerNameTextRect)

            sumText = Font.make("GaramondBold", 20).render("Sum:", 1, Color.WHITE)
            self.screen.blit(sumText, sumText.get_rect(topleft=(self.shieldsImageStartX[playerIndex] + 54, 144)))
            playerSumText = Font.make("GaramondBold", 30).render(str(sum(map(int, self.getCardsOfPlayer(playerIndex)))), 1, Color.WHITE)
            self.screen.blit(playerSumText, playerSumText.get_rect(topleft=(self.shieldsImageStartX[playerIndex] + 106, 137)))

            trunReminingText = Font.make("GaramondBold", 17).render("Turns reamining:", 1, Color.WHITE)
            self.screen.blit(trunReminingText, trunReminingText.get_rect(topleft=(self.shieldsImageStartX[playerIndex] + 25, 187)))
            trunReminingText = Font.make("GaramondBold", 17).render(str(Game.playerMaxTurn-self.playedTurns[playerIndex]), 1, Color.WHITE)
            self.screen.blit(trunReminingText, trunReminingText.get_rect(midtop=(self.shieldsImageStartX[playerIndex] + 90, 207)))

        if winner:
            self.ended = True
            gameStatusText = f"{winner.name} wins"
        elif sum(self.playedTurns) == Game.playerMaxTurn * 2:
            self.ended = True
            gameStatusText = f"Tie"
        else:
            gameStatusText = f"{self.players[self.turn].name}'s turn"
        text = Font.make("GaramondBold", 30).render(gameStatusText, 1, Color.ORANGE)
        textRect = text.get_rect()
        textRect.midtop = (511, 540)
        self.screen.blit(text, textRect)


    def play(self, event):
        clickedCard = self.getClickedCard(event.pos)
        turnPlayerCards = self.getCardsOfPlayer(self.turn)
        if clickedCard:
            if clickedCard.statusOnBoard[0] == 0 and len(turnPlayerCards) < 3:
                clickedCard.statusOnBoard = [self.turn + 1, len(turnPlayerCards)]
                self.nextTurn()
                return True

            elif (clickedCard.statusOnBoard[0] == 0) or (clickedCard.statusOnBoard[0] == self.turn + 1 and len(turnPlayerCards) == 3):
                if self.selectedCard == None:
                    clickedCard.setSelected()
                    self.selectedCard = clickedCard

                elif clickedCard == self.selectedCard:
                    self.selectedCard.setUnSelected()
                    self.selectedCard = None

                elif clickedCard.statusOnBoard[0] == self.selectedCard.statusOnBoard[0]:
                    self.selectedCard.setUnSelected()
                    clickedCard.setSelected()
                    self.selectedCard = clickedCard

                else:
                    self.selectedCard.statusOnBoard, clickedCard.statusOnBoard = clickedCard.statusOnBoard, self.selectedCard.statusOnBoard
                    self.selectedCard.setUnSelected()
                    self.selectedCard = None
                    self.nextTurn()

                return True

        return False