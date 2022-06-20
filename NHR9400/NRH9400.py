import random
import socket
from Utility import IPFinder

class NHR9400:
    
    def __init__(self, name):
        self.__name = name
        self.__s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__s.timeout(1)
        pass

    

    def setIp(self):
        pass
    def getIp(self):
        pass
    #Function to see if exist any error in the carry
    def checkErrors(self):
        self.__s.send("SYSTem:ERRor?")
    #set limit voltage of all channels
    def setVoltage(self,voltage):
        self.__s.send("SOUR:VOLT " + voltage + "\n")
    
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

    