import importlib.util

class Player:
    def __init__(self, name, mode, filePath=""):
        self.name = name
        self.mode = mode
        if self.mode == "Agent":
            self.filePath = filePath
            spec = importlib.util.spec_from_file_location("module.name", self.filePath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.mainFunction = module.main

    def isHuman(self):
        return self.mode == "Human"

    @staticmethod
    def isCodeFileValid(filePath):
        try:
            spec = importlib.util.spec_from_file_location("module.name", filePath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.main([2, 5], [1, 8], [3, 4, 6, 7])
            return True
        except:
            return False