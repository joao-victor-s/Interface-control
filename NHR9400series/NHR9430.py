from NHR9400series.NHR9400 import NHR9400

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

    #Fetch the average current of all channels
    def getCurrent(self):
        value = self.__s.send("FETC:CURR?\n")
        return self.receiveFloat(value)
    #fetch individual value of current of one channel
    def getCurrentA(self):
        value = self.__s.send("FETC:CURR:APHase?\n")
        return self.receiveFloat(value)
    def getCurrentB(self):
        value = self.__s.send("FETC:CURR:BPHase?\n")
        return self.receiveFloat(value)
    def getCurrentC(self):
        value = self.__s.send("FETC:CURR:CPHase?\n")
        return self.receiveFloat(value)
    
    def locateIp(self,clients = []):
        for client in clients:
            try:
                self.__s.connect((client, 5025))
                self.__s.send("SYST:RWL\n") #Command to activate remote control and locking the touchscreen
                self.__s.send("*IDN?\n")
                recv = super().receiveString()
                if recv.find("NH Research,9430-") != -1: #if find this subtring 
                    self.__ip = client
                    print("Connection successfully")
                    break
                else:
                    print("Connection failed 1")
                    self.__s.close()
            except:
                print("Connection failed 2")
                pass
            


    
