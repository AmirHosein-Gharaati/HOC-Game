import pygame

import time

from .card import Card
from .color import Color
from .font import Font
from .scroll_text_box import ScrollTextBox

class Game:
    playerMaxTurn = 30

    def __init__(self, screen, players, agentDelayTime, startTurnIndex, agentVSagentPageMode):
        self.screen = screen
        self.players = players
        self.cards = [Card(screen, cardNumber) for cardNumber in range(1, 9)]
        self.playedTurns = [0, 0]
        self.agentPlayedInvalid = [False, False]
        self.selectedCard = None
        self.turn = self.startTurnIndex = int(startTurnIndex)
        self.ended = False
        self.isBothAgent = all(not player.isHuman() for player in self.players)
        self.agentDelayTime = agentDelayTime
        self.agentVSagentPageMode = agentVSagentPageMode

        self.textBox = ScrollTextBox(self.screen, Font.make("Garamond", 30), 106, 120, 480)
        self.initializeImage()

    def reset(self):
        self.cards = [Card(self.screen, cardNumber) for cardNumber in range(1, 9)]
        self.playedTurns = [0, 0]
        self.agentPlayedInvalid = [False, False]
        self.selectedCard = None
        self.turn = self.startTurnIndex = 1 ^ self.startTurnIndex
        self.ended = False

    def noHuman(self):
        return self.isBothAgent

    def initializeImage(self):
        self.shieldsTurnImage = pygame.image.load("images/ShieldTurn.png")
        self.shieldsOtherImage = pygame.image.load("images/ShieldOther.png")
        self.shieldsImageStartX = [21, 822]

    def nextTurn(self):
        self.playedTurns[self.turn] += 1
        self.turn ^= 1

    def isAgentResponseValid(self, response, gameCards):
        if len(response) == 2:
            selected, unselected = response
            if selected in gameCards[2]:
                if (len(gameCards[0]) == 3 and unselected in gameCards[0]) or (len(gameCards[0]) < 3 and unselected == 0):
                    return True
        return False

    def agentPlay(self):
        time.sleep(self.agentDelayTime)

        gameCards = tuple([tuple([int(card) for card in self.getCardsOfPlayer(index)]) for index in (self.turn, self.turn ^ 1, -1)])
        agentResponse = self.players[self.turn].mainFunction(*gameCards)
        if not self.isAgentResponseValid(agentResponse, gameCards):
            self.agentPlayedInvalid[self.turn] = True
            if self.noHuman():
                self.textBox.add(f"{self.players[self.turn].name} made an invalid move", Color.RED2)
                winner = self.getWinner()
                self.ended = True
                self.textBox.add(f"  $  {winner.name} won  $", Color.DEEPSKYBLUE2, center=True)
            return
        else:
            selected, unselected = agentResponse

        if unselected:
            self.cards[selected - 1].statusOnBoard, self.cards[unselected - 1].statusOnBoard = self.cards[unselected - 1].statusOnBoard, self.cards[selected - 1].statusOnBoard
            logText = f"{self.players[self.turn].name} replaced card {selected} with {unselected}"
        else:
            self.cards[selected - 1].statusOnBoard = [self.turn + 1, len(self.getCardsOfPlayer(self.turn))]
            logText = f"{self.players[self.turn].name} picked card {selected}"

        if self.noHuman():
            logText += f"  |  Cards: {' ,  '.join(map(lambda card: str(int(card)), self.getCardsOfPlayer(self.turn)))}"
            logText += f"  |  Sum: {self.getSumCardsOfPlayer(self.turn)}"
            logColor = Color.GREEN2 if self.turn % 2 else Color.ORANGE
            self.textBox.add(logText, logColor)

            winner = self.getWinner()
            if winner:
                self.ended = True
                self.textBox.add(f"  $  {winner.name} won  $", Color.DEEPSKYBLUE2, center=True)

            elif sum(self.playedTurns) == Game.playerMaxTurn * 2:
                self.ended = True
                self.textBox.add("  $  Tie  $", Color.DEEPSKYBLUE2, center=True)

    def getClickedCard(self, position):
        return next((card for card in self.cards if card.collidepoint(position)), None)

    def getCardsOfPlayer(self, playerIndex):
        return [card for card in self.cards if card.statusOnBoard[0] - 1 == playerIndex]

    def getSumCardsOfPlayer(self, playerIndex):
        return sum(map(int, self.getCardsOfPlayer(playerIndex)))

    def isEnded(self):
        if not self.ended and self.getWinner():
            self.ended = True
        return self.ended

    def getWinner(self):
        for playerIndex in (0, 1):
            if len(self.getCardsOfPlayer(playerIndex)) == 3 and self.getSumCardsOfPlayer(playerIndex) == 15:
                return self.players[playerIndex]
            elif self.agentPlayedInvalid[playerIndex]:
                return self.players[playerIndex^1]
        return None

    def show(self):
        if self.noHuman() and self.agentVSagentPageMode == "Console":
            self.textBox.show()
            return

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
            playerSumText = Font.make("GaramondBold", 30).render(str(self.getSumCardsOfPlayer(playerIndex)), 1, Color.WHITE)
            self.screen.blit(playerSumText, playerSumText.get_rect(topleft=(self.shieldsImageStartX[playerIndex] + 106, 137)))

            trunReminingText = Font.make("GaramondBold", 17).render("Turns reamining:", 1, Color.WHITE)
            self.screen.blit(trunReminingText, trunReminingText.get_rect(topleft=(self.shieldsImageStartX[playerIndex] + 25, 187)))
            trunReminingText = Font.make("GaramondBold", 17).render(str(Game.playerMaxTurn-self.playedTurns[playerIndex]), 1, Color.WHITE)
            self.screen.blit(trunReminingText, trunReminingText.get_rect(midtop=(self.shieldsImageStartX[playerIndex] + 90, 207)))

        if winner:
            self.ended = True
            gameStatusText = f"{winner.name} won"
        elif sum(self.playedTurns) == Game.playerMaxTurn * 2:
            self.ended = True
            gameStatusText = f"Tie"
        else:
            gameStatusText = f"{self.players[self.turn].name}'s turn"
        text = Font.make("GaramondBold", 30).render(gameStatusText, 1, Color.ORANGE2)
        textRect = text.get_rect()
        textRect.midtop = (511, 540)
        self.screen.blit(text, textRect)

    def play(self, event):
        if self.noHuman():
            self.textBox.update(event)
            return True

        if self.isEnded():
            return False

        if self.players[self.turn].mode == "Agent":
            self.agentPlay()
            self.nextTurn()
            return True

        elif event.type != pygame.MOUSEBUTTONDOWN:
            return False

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