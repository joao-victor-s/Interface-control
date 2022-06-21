import random
import socket
from Utility import IPFinder, RefineOutput


class NHR9400:
    
    def __init__(self, name):
        self.__name = name
        self.__s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__s.timeout(1)
        self.__out = RefineOutput


    def setIp(self):
        pass
    def getIp(self):
        pass

    #Function that receives messages back and transform it in a string
    def receiveString(self):
        msg = self.__s.recv(1024)
        msg = self.__out.RefineOutput.byteToString(msg)
        return msg
    
    #Function that receives messages back and transform it in a float
    def receiveFloat(self):
        msg = self.__s.recv(1024)
        msg = self.__out.RefineOutput.byteToFloat(msg)
        return msg

    def identify(self):
        self.__s.send("*IDN?\n")
        return self.receive()

    def checkErrors(self):
        self.__s.send("SYST:ERR?\n")
        return self.receive()

    #Function to see if exist any error in the carry
    def checkErrors(self):
        self.__s.send("SYSTem:ERRor?")
    #set limit voltage of all phases
    def setVoltage(self,voltage):
        self.__s.send("SOUR:VOLT " + voltage + "\n")
    
    #set the current of all phases ** Available only to NHR9430-12
    def setCurrent(self, current):
        self.__s.send("SOUR:CURR " + current + "\n")

    def setPower(self, pow):
        self.__s.send("SOUR:POW " + pow + "\n")
    def setFreq(self, freq):
        self.__s.send("SOUR:POW " + freq + "\n")

    def getVoltage(self):
        value = self.__s.send("FETCh:VOLTage?")
        
        
    def getCurrent():
    
    def getPower():
    
    def getFreq():

    