from NHR9400series.NHR9400 import NHR9400
from Utility import IPFinder

class NHR9410(NHR9400):

    def __init__(self):
        super().__init__("NHR9410")
    
    def getIp(self):
        return super().getIp()

    
