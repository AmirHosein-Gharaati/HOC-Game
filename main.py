if __name__ == "__main__":
    import sys
    from os import environ
    environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
    import pygame
    pygame.init()

    from pages.help_page import HelpPage
    from pages.main_page import MainPage
    from pages.play_menu_page import PlayMenuPage
    from pages.play_page import PlayPage

    class Game:
        def __init__(self):
            self.screen = pygame.display.set_mode((1022, 700))
            pygame.display.set_caption("15")

            self.mainPage = MainPage(self.screen)
            self.helpPage = HelpPage(self.screen)
            self.playMenuPage = PlayMenuPage(self.screen)
            self.playPage = PlayPage(self.screen)

            self.pageStatus = "Main"

        def run(self):
            while self.pageStatus != "Exit":
                if self.pageStatus == "Main":
                    self.mainPage.show()
                    self.pageStatus = self.mainPage.run()

                elif self.pageStatus == "Help":
                    self.helpPage.show()
                    self.pageStatus = self.helpPage.run()

                elif self.pageStatus == "Play":
                    self.playMenuPage.initializeButtons()
                    self.playMenuPage.show()
                    self.pageStatus, players = self.playMenuPage.run()

                elif self.pageStatus == "Start":
                    self.playPage.newGame(players)
                    self.playPage.show()
                    self.pageStatus = self.playPage.run()

            pygame.quit()

    Game().run()
    sys.exit(0)