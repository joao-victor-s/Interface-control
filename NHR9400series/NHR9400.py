from abc import abstractmethod
import socket
from Utility.RefineOutput import RefineOutput
from Utility.IPFinder import IPFinder


class NHR9400:
    
    def __init__(self, name):
        self.__name = name
        self.__s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__s.settimeout(1)
        self.__out = RefineOutput


    @abstractmethod
    def locateIp(self):
        pass


    #Function that receives messages back and transform it in a string
    def receiveString(self):
        msg = self.__s.recv(1024)
        msg = self.__out.byteToString(msg)
        return msg
    
    #Function that receives messages back and transform it in a float
    def receiveFloat(self):
        msg = self.__s.recv(1024)
        msg = self.__out.byteToFloat(msg)
        return msg

    def identify(self):
        self.__s.send("*IDN?\n")
        return self.receive()
    #Function to see if exist any error in the carry
    def checkErrors(self):
        self.__s.send("SYST:ERR?\n")
        return self.receive()

    #set limit voltage of all phases
    def setVoltage(self,voltage):
        self.__s.send("SOUR:VOLT " + voltage + "\n")
    #Functions that sets the limits voltage on one phase (A, B or C)
    def setVoltageA(self,voltage):
        self.__s.send("SOUR:VOLT:APHase " + voltage + "\n")

    def setVoltageB(self,voltage):
        self.__s.send("SOUR:VOLT:BPHase " + voltage + "\n")

    def setVoltageC(self,voltage):
        self.__s.send("SOUR:VOLT:CPHase " + voltage + "\n")

    #Command establishes the True Power limit (W) as a positive value for the selected instrument.
    def setPower(self, pow):
        self.__s.send("SOUR:POW " + pow + "\n")
    #Individual command for one phase
    def setPowerA(self, pow):
        self.__s.send("SOUR:POW:APHase " + pow + "\n")
    def setPowerB(self, pow):
        self.__s.send("SOUR:POW:BPHase " + pow + "\n")
    def setPowerC(self, pow):
        self.__s.send("SOUR:POW:CPHase " + pow + "\n")
    #Command establishes the operating frequency for the selected instrument.
    def setFreq(self, freq):
        self.__s.send("SOUR:POW " + freq + "\n")
    #Fetch the average voltage of all channels
    def getVoltage(self):
        value = self.__s.send("FETC:VOLT?\n")
        return self.receiveFloat(value)
    #fetch individual value of voltage of one channel
    def getVoltageA(self):
        value = self.__s.send("FETC:VOLT:APHase?\n")
        return self.receiveFloat(value)
    def getVoltageB(self):
        value = self.__s.send("FETC:VOLT:BPHase?\n")
        return self.receiveFloat(value)
    def getVoltageC(self):
        value = self.__s.send("FETC:VOLT:CPHase?\n")
        return self.receiveFloat(value)
        
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
    #Fetch the average power of all channels
    def getPower(self):
        value = self.__s.send("FETC:POW?\n")
        return self.receiveFloat(value)
    #fetch individual value of Power of one channel
    def getPowerA(self):
        value = self.__s.send("FETC:POW:APHase?\n")
        return self.receiveFloat(value)
    def getPowerB(self):
        value = self.__s.send("FETC:POW:BPHase?\n")
        return self.receiveFloat(value)
    def getPowerC(self):
        value = self.__s.send("FETC:POW:CPHase?\n")
        return self.receiveFloat(value)
