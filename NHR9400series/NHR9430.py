from NHR9400series.NHR9400 import NHR9400

class NHR9430(NHR9400):

    def __init__(self):
        super().__init__("NHR9410")

    #Command sets the loading features <loading mode> for a 9430 AC output Query returns the loading features enabled on a 9430
    #Command is only accepted if the instrument is a 9430, with AC outputs mode, and in an OFF state Other models & modes: This command is invalid
    # 0 = NORMal = CC / CP / CVA with modifiers (PF, CF, & IWAVESHAPE)
    # 1 = CR = Constant Resistance (with optional CC limit)
    # 2 = RL = Constant series Resistance & Inductance
    def instrumentLoad(self, value):
        if value < 0 or value > 2:
            print("INVALID INPUT")
        else:
            if value == 0:
                self.__s.send("CONF:INST:LOAD:NORM")
            if value == 1:
                self.__s.send("CONF:INST:LOAD:CR")
            if value == 2:
                self.__s.send("CONF:INST:LOAD:RL")
        self.checkErrors()
            
    #Command enables bi-directional power flow for the 9420 (DC outputs) and 9430 (AC outputs) Query returns if Bi-directional power flow is permitted.
    #0 | NO | FALSE | OFF = Bi directional mode is disabled 
    #1 | YES | TRUE | ON = Bi directional mode is enabled
    def instrumentBidirec(self, value):
        if value == 0 or value == 1:
            self.__s.send("CONF:INST:BID"+ str(value) + "\n")
        else:
            print("INVALID INPUT")
        self.checkErrors()
    #Command sets the standby detection conditions. 
    #Query returns the configured standby detection conditions for the selected instrument
    def instrumentStndy(self):
         self.__s.send("CONF: INST:STBY")
         self.checkErrors()

    #set the current of all phases ** Available only to NHR9430-12
    def setCurrent(self, current):
        self.__s.send("SOUR:CURR " + str(current) + "\n")
    #Functions that sets the limite currents on one phase (A, B or C)
    def setCurrentA(self, current):
        self.__s.send("SOUR:CURR:APHase " + str(current) + "\n")
    def setCurrentB(self, current):
        self.__s.send("SOUR:CURR:BPHase " + str(current) + "\n")
    def setCurrentC(self, current):
        self.__s.send("SOUR:CURR:CPHase " + str(current) + "\n")

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
                    return self.__ip
                else:
                    print("Connection failed 1")
                    self.__s.close()
            except:
                print("Connection failed 2")
                pass
            


    
