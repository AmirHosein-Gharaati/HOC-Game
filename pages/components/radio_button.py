import pygame

from .color import Color
from .font import Font

class RadioButton:
    class OptionButton:
        def __init__(self, screen, name, startX, startY, radius, font, checkBoxLeft):
            self.screen = screen
            self.name = name
            self.startX = startX
            self.startY = startY
            self.font = font
            self.radius = radius
            self.checked = False
            self.checkBoxLeft = checkBoxLeft
            self.circlesCenterPosition = (self.startX+self.radius, self.startY+self.radius)
        
        def isChecked(self):
            return self.checked
            
        def setChecked(self):
            self.checked = True
            self.showCheck()
            
        def setUnChecked(self):
            self.checked = False
            self.showCheck()
        
        def showCheck(self):
            pygame.draw.circle(self.screen, Color.WHITE, self.circlesCenterPosition, self.radius-3)
            if self.checked: pygame.draw.circle(self.screen, Color.RED, self.circlesCenterPosition, self.radius-6)
        
        def show(self):
            self.area = pygame.draw.circle(self.screen, Color.BLACK, self.circlesCenterPosition, self.radius)
            self.showCheck()
            
            if self.checkBoxLeft:
                self.screen.blit(self.font.render(self.name, 1, Color.BLACK), (self.startX+self.radius*2+5, self.startY-6))
                
            else:
                text = self.font.render(self.name, True, Color.BLACK)
                text_rect = text.get_rect()
                text_rect.topright = (self.startX-5, self.startY-6)
                self.screen.blit(text, text_rect)            
        
        def collidepoint(self, position):
            return self.area.collidepoint(position)
    
    def __init__(self, screen, optionsName, startX, startY, checkBoxLeft=True):
        self.screen = screen
        self.startX = startX
        self.startY = startY
        self.checkBoxLeft = checkBoxLeft
        self.initializeButtons(optionsName)
        
    def initializeButtons(self, optionsName):
        self.optionsButton = []
        Garamond30Font = Font.make("Garamond", 30)
        
        for index, optionName in enumerate(optionsName):
            optionButton = RadioButton.OptionButton(self.screen, optionName, self.startX, self.startY+index*45, 15, Garamond30Font, self.checkBoxLeft)
            self.optionsButton.append(optionButton)
        
        self.optionsButton[0].setChecked()
        
    def show(self):
        for optionButton in self.optionsButton:
            optionButton.show()
        pygame.display.flip()
    
    def collidepoint(self, position):
        return any(optionButton.collidepoint(position) for optionButton in self.optionsButton)
    
    def update(self, position):
        for optionButton in self.optionsButton:
            if optionButton.collidepoint(position):
                optionButton.setChecked()
            else:
                optionButton.setUnChecked()
        pygame.display.flip()
    
    def selected(self):
        for optionButton in self.optionsButton:
            if optionButton.isChecked():
                return optionButton.name
        return None
            