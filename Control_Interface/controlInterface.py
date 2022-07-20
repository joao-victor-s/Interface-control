import sys
sys.path.insert(0, "..")

from NHR9400series.NHR9410 import NHR9410
from NHR9400series.NHR9430 import NHR9430
from Utility.IPFinder import IPFinder

class controlInterface:
    
    def __init__(self):
        self.__listIp = IPFinder().getList()
        self.__listUsedIp = []
        self.__nhr9410 = []
        self.__nhr9430 = []

    #refresh the list of ip
    def refresh(self):
        self.__listIp = IPFinder().getList()
        for ip in self.__listUsedIp:
            self.__listIp.remove(ip)
    
    #create a NHR9410 object
    def newNhr9410(self):
        new = NHR9410()
        new.__init__()
        new.locateIp(self.__listIp)

        usedIp = new.getIp()
        print(type(usedIp))
        try:
            self.__listIp.remove(usedIp)
            self.__listUsedIp.append(usedIp)
            self.__nhr9430.append(new)
        except:
            print("Any IP adress matched")
    
    #create a NHR9430 object
    def newNhr9430(self):
        new = NHR9430()
        new.__init__()
        usedIp = new.locateIp(self.__listIp)
        #print(usedIp)
        try:
            self.__listIp.remove(usedIp)
            self.__listUsedIp.append(usedIp)
            self.__nhr9430.append(new)
        except:
            print("Any IP adress matched")

    def getNhr9410(self):
        return self.__nhr9410
        
    def getNhr9430(self):
        return self.__nhr9430

    def getListIp(self):
        return self.__listIp
