import random
import socket
from Utility import IPFinder

class NHR9400:
    
    def __init__(self, name):
        self.__id = random.randrange(100, 300, 2)
        self.__name = name
        self.__s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__s.timeout(1)

    

    def setIp(self):
        pass
    #Function to see if exist any error in the carry
    def checkErrors(self):
        self.__s.send("SYSTem:ERRor?")
    #set limit voltage of all channels
    def setVoltage(self,voltage):
        self.__s.send("VOLT " + voltage + "\n")
    
    def setCurrent(self, current):
        self.__s.send("CURR " + current + "\n")
    def setPower():
    
    def setFreq():

    def getVoltage(self):
        value = self.__s.send("FETCh:VOLTage?")
        
        
    def getCurrent():
    
    def getPower():
    
    def getFreq():

    