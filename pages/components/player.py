class Player:
    def __init__(self, name, mode, filePath=""):
        self.name = name
        self.mode = mode
        if self.mode == "Agent":
            self.filePath = filePath
            self.mainFunction = __import__(self.filePath).main

    def isHuman(self):
        return self.mode == "Human"