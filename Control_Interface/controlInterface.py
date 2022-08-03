
from NHR9400series.NHR9410 import NHR9410
from NHR9400series.NHR9430 import NHR9430
from UtilitiesRei.IPFinder import IPFinder

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
    
    #create a NHR object 
    def newNhr(self, nhr):
        if(nhr == "9410"):
            new = NHR9410()
        elif nhr == "9430":
            new = NHR9430()
        else:
            return -1
        new.locateIp(self.__listIp)
        print(new.getIp())
        print(new.getS())
        
        usedIp = new.getIp()
        print("usedIP:" + str(usedIp))
        try:
            self.__listIp.remove(usedIp)
            self.__listUsedIp.append(usedIp)
            if nhr == "9410":
                self.__nhr9410.append(new)
            elif nhr == "9430":
                self.__nhr9430.append(new)
            else:
                return -1
        except:
            print("Any IP address matched")

    def getNhr9410(self):
        return self.__nhr9410
        
    def getNhr9430(self):
        return self.__nhr9430

    def getListIp(self):
        return self.__listIp
