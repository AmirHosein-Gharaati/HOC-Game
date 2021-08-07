class Player:
    def __init__(self, name, mode, filePath=""):
        self.name = name
        self.mode = mode
        if self.mode == "Agent":
            self.filePath = filePath
            self.mainFunction = __import__(self.filePath).main

    def isHuman(self):
        return self.mode == "Human"

    @staticmethod
    def isCodeFileValid(filePath):
        try:
            __import__(filePath).main([2, 5], [1, 8], [3, 4, 6, 7])
            return True
        except Exception as e:
            print(e)
            return False