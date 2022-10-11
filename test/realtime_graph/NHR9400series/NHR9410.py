from NHR9400series.NHR9400 import NHR9400

class NHR9410(NHR9400):

    def __init__(self):
        super().__init__("9410")

    def setS(self):
        self.__s = self.getS()
    
