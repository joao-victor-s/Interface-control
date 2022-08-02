from NHR9400series.NHR9400 import NHR9400

class NHR9430(NHR9400):

    def __init__(self):
        super().__init__("NHR9430")
        self.__ip = ""

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
                self.__s.send("CONF:INST:LOAD:NORM".encode())
            if value == 1:
                self.__s.send("CONF:INST:LOAD:CR".encode())
            if value == 2:
                self.__s.send("CONF:INST:LOAD:RL".encode())
        self.checkErrors()
            
    #Command enables bi-directional power flow for the 9420 (DC outputs) and 9430 (AC outputs) Query returns if Bi-directional power flow is permitted.
    #0 | NO | FALSE | OFF = Bi directional mode is disabled 
    #1 | YES | TRUE | ON = Bi directional mode is enabled
    def instrumentBidirec(self, value):
        if value == 0 or value == 1:
            self.__s.send(("CONF:INST:BID"+ str(value) + "\n").encode())
        else:
            print("INVALID INPUT")
        self.checkErrors()
    #Command sets the standby detection conditions. 
    #Query returns the configured standby detection conditions for the selected instrument
    def instrumentStndy(self):
         self.__s.send("CONF: INST:STBY".encode())
         self.checkErrors()

    #set the current of all phases ** Available only to NHR9430-12
    def setCurrent(self, current):
        self.__s.send(("SOUR:CURR " + str(current) + "\n").encode())
    #Functions that sets the limite currents on one phase (A, B or C)
    def setCurrentA(self, current):
        self.__s.send(("SOUR:CURR:APHase " + str(current) + "\n").encode())
    def setCurrentB(self, current):
        self.__s.send(("SOUR:CURR:BPHase " + str(current) + "\n").encode())
    def setCurrentC(self, current):
        self.__s.send(("SOUR:CURR:CPHase " + str(current) + "\n").encode())

    #Fetch the average current of all channels
    def getCurrent(self):
        value = self.__s.send("FETC:CURR?\n".encode())
        return self.receiveFloat(value)
    #fetch individual value of current of one channel
    def getCurrentA(self):
        value = self.__s.send("FETC:CURR:APHase?\n".encode())
        return self.receiveFloat(value)
    def getCurrentB(self):
        value = self.__s.send("FETC:CURR:BPHase?\n".encode())
        return self.receiveFloat(value)
    def getCurrentC(self):
        value = self.__s.send("FETC:CURR:CPHase?\n".encode())
        return self.receiveFloat(value)
    
    def getIp(self):
        return self.__ip


    
