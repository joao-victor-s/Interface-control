from NHR9400series.NHR9400 import NHR9400

class NHR9410(NHR9400):

    def __init__(self):
        super().__init__("NHR9410")
        self.__ip = ""
    
    def getIp(self):
        return self.__ip



    
