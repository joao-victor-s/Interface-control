from NHR9400series.NHR9400 import NHR9400
from Utility.RefineOutput import RefineOutput

class NHR9430(NHR9400):

    def __init__(self):
        super().__init__("NHR9410")

    #set the current of all phases ** Available only to NHR9430-12
    def setCurrent(self, current):
        self.__s.send("SOUR:CURR " + current + "\n")
    #Functions that sets the limite currents on one phase (A, B or C)
    def setCurrentA(self, current):
        self.__s.send("SOUR:CURR:APHase " + current + "\n")
    def setCurrentB(self, current):
        self.__s.send("SOUR:CURR:BPHase " + current + "\n")
    def setCurrentC(self, current):
        self.__s.send("SOUR:CURR:CPHase " + current + "\n")
    
    def locateIp(self,clients = []):
        for client in clients:
            try:
                self.__s.connect((client, 5025))
                self.__s.send("SYST:RWL\n") #Command to activate remote control and locking the touchscreen
                self.__s.send("*IDN?\n")
                recv = super().receiveString()
                if recv.find("NH Research,9430-") != -1: #if find this subtring 
                    self.__ip = client
                    clients.remove(client)
                    break
                else:
                    self.__s.close()
            except:
                pass
            


    
