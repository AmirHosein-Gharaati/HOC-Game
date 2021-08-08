import pygame

class Font:
    baseFolder = "fonts/"

    fontDict = {"Garamond": f"{baseFolder}EBGaramond-VariableFont_wght.ttf",
                "GaramondBold": f"{baseFolder}EBGaramond-Bold.ttf",
                "Algerian": f"{baseFolder}Algerian Regular.ttf",
                None: None}

    @staticmethod
    def make(name, size):
        return pygame.font.Font(Font.fontDict[name], size)