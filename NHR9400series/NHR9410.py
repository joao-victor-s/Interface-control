from NHR9400series.NHR9400 import NHR9400

class NHR9410(NHR9400):

    def __init__(self):
        super().__init__("9410")

    def getS(self):
        return self.__s
    
