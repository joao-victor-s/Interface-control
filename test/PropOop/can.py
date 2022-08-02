import mug

class can(mug.mug):
    
    def __init__(self, name):
        super().__init__(name)
        self.__id = 0

    def setId(self, id):
        self.__id = id
    
    def getId(self):
        return self.__id