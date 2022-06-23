from NHR9400series.NHR9400 import NHR9400
from Utility.RefineOutput import RefineOutput

class NHR9430(NHR9400):

    def __init__(self):
        super().__init__("NHR9410")
    
    def locateIp(self,clients = []):
        for client in clients:
            self.__s.connect((client, 5025))
            self.__s.send("SYST:RWL\n") #Command to activate remote control and locking the touchscreen
            self.__s.send("*IDN?\n")
            recv = super().receiveString()
            if recv.find("NH Research,9410-") != -1: #if find this subtring 
                self.__ip = client
                clients.remove(client)
                break
            else:
                self.__s.close()


    
