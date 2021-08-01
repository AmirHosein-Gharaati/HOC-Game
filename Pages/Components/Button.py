import pygame
from .Color import Color

class Button:
    def __init__(self, sizes, color, name, font, screen):
        self.sizes = sizes
        self.color = color
        self.name = name
        self.font = font
        self.screen = screen
        
    def show(self):
        border = pygame.draw.rect(self.screen,
                                  Color.BLACK,
                                  [self.sizes[0]-3, self.sizes[1]-3,
                                   self.sizes[2]+6, self.sizes[3]+6],
                                  border_radius=6)
        rect = pygame.draw.rect(self.screen, self.color, self.sizes, border_radius=4)
        
        text = self.font.render(self.name, 1, Color.BLACK)
        textRect = text.get_rect(center=(self.sizes[0]+self.sizes[2]/2,
                                         self.sizes[1]+self.sizes[3]/2-3))
        self.screen.blit(text, textRect)
        
        self.area = border
    
    def collidepoint(self, position):
        return self.area.collidepoint(position)