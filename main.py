import sys
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pygame.locals import *

class Color:
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    RED = (255, 90, 90)
    BLUE = (50, 125, 200)

class Button:
    def __init__(self, sizes, color, name, font):
        self.sizes = sizes
        self.color = color
        self.name = name
        self.font = font
        
    def show(self):
        border = pygame.draw.rect(screen,
                                  Color.BLACK,
                                  [self.sizes[0]-3, self.sizes[1]-3,
                                   self.sizes[2]+6, self.sizes[3]+6],
                                  border_radius=6)
        rect = pygame.draw.rect(screen, self.color, self.sizes, border_radius=4)
        
        text = self.font.render(self.name, 1, Color.BLACK)
        textRect = text.get_rect(center=(self.sizes[0]+self.sizes[2]/2,
                                         self.sizes[1]+self.sizes[3]/2-3))
        screen.blit(text, textRect)
        
        self.area = border
    
    def collidepoint(self, position):
        return self.area.collidepoint(position)

class MainPage:
    def __init__(self):
        self.initializeImages()
        self.initializeFonts()
        self.initializeButtons()
    
    def show(self):
        screen.blit(self.mainBackgroundImage, (0, 0))
        
        screen.blit(self.Algerian116Font.render("FIFTEEN", 1, Color.BLACK), (290, 0))
        screen.blit(self.card15Image, (423, 121))
        
        for button in self.buttons: button.show()
        
        pygame.display.flip()
    
    def initializeButtons(self):
        gameButtonsName = ("Human vs Human", "Human vs Agent", "Agent vs Agent")
        self.buttons = []
        for buttonIndex, buttonName in enumerate(gameButtonsName):
            gameButton = Button((321, buttonIndex*78+264, 380, 70),
                                Color.GRAY,
                                buttonName,
                                self.Garamond45Font)
            self.buttons.append(gameButton)
        
        self.buttons.append(Button((530, 512, 112, 44), Color.RED, "Exit", self.Garamond30Font))
        
        self.buttons.append(Button((390, 512, 112, 44), Color.BLUE, "Help", self.Garamond30Font))
    
    def initializeImages(self):
        self.mainBackgroundImage = pygame.image.load("images/MainBackground.png")
        self.card15Image = pygame.image.load("images/cards/15.png")
    
    def initializeFonts(self):
        self.Garamond30Font = pygame.font.Font("fonts/EBGaramond-VariableFont_wght.ttf", 30)
        self.Garamond45Font = pygame.font.Font("fonts/EBGaramond-VariableFont_wght.ttf", 40)
        self.Algerian116Font = pygame.font.Font("fonts/Algerian Regular.ttf", 116)
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "Exit"
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.collidepoint(pygame.mouse.get_pos()):
                            return button.name

class HelpPage:
    def __init__(self):
        self.initializeFonts()
        self.initializeImages()
        self.initializeButtons()
    
    def show(self):
        screen.blit(self.mainBackgroundImage, (0, 0))
        
        screen.blit(self.Algerian116Font.render("FIFTEEN", 1, Color.BLACK), (290, 0))
        
        self.mainPageButton.show()
        
        pygame.display.flip()
    
    def initializeButtons(self):
        self.mainPageButton = Button((445, 512, 132, 44), Color.RED, "Main Page", self.Garamond30Font)
    
    def initializeImages(self):
        self.mainBackgroundImage = pygame.image.load("images/MainBackground.png")
    
    def initializeFonts(self):
        self.Garamond30Font = pygame.font.Font("fonts/EBGaramond-VariableFont_wght.ttf", 30)
        self.Algerian116Font = pygame.font.Font("fonts/Algerian Regular.ttf", 116)
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "Exit"
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mainPageButton.collidepoint(pygame.mouse.get_pos()):
                        return "Main"

class Game:
    def __init__(self):
        global screen
        
        pygame.init()
        screen = pygame.display.set_mode((1022, 700))
        pygame.display.set_caption("15")
    
        self.mainPage = MainPage()
        self.helpPage = HelpPage()
        
    def run(self):
        situation = "Main"
        while situation != "Exit":
            if situation == "Main":
                self.mainPage.show()
                situation = self.mainPage.run()
            
            elif situation == "Help":
                self.helpPage.show()
                situation = self.helpPage.run()
            
            elif situation == "Human vs Human":
                situation = "Main"
            
            elif situation == "Human vs Agent":
                situation = "Main"
            
            elif situation == "Agent vs Agent":
                situation = "Main"
        
        pygame.quit()

Game().run()
sys.exit(0)