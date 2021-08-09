import random


def main(myCards, opponentCards, onBoardCards):
    selected = random.choice(onBoardCards)
    unselected = random.choice(myCards) if len(myCards) == 3 else 0

    return selected, unselected
