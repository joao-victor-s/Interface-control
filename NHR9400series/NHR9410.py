from NHR9400series.NHR9400 import NHR9400


class NHR9410(NHR9400):

    def __init__(self):
        super().__init__("NHR9410")
    
    def locateIp(self,clients = []):
        for client in clients:
            try:
                self.__s.connect((client, 5025))
                self.__s.send("SYST:RWL\n") #Command to activate remote control and locking the touchscreen
                self.__s.send("*IDN?\n")
                recv = super().receiveString()
                if recv.find("NH Research,9410-") != -1: #if find this subtring 
                    self.__ip = client
                    print("Connection successfully")
                    return self.__ip
                else:
                    print("Connection failed 1")
                    self.__s.close()
            except:
                print("Connection failed 2")



    
