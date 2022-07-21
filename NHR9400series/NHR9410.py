from NHR9400series.NHR9400 import NHR9400
import socket

class NHR9410(NHR9400):

    def __init__(self):
        super().__init__("NHR9410")
        self.__ip = 0
    
    def locateIp(self,clients = []):
        for client in clients:
            try:
                self.__s  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.__s.settimeout(1)
                self.__s.connect((client, 5025))
                self.__s.send("SYST:RWL\n".encode()) #Command to activate remote control and locking the touchscreen
                self.__s.send("*IDN?\n".encode())
                msg = self.__s.recv(1024)
                recv = self.receiveString(msg)
                if recv.find("NH Research,9410-") != -1: #if find this subtring 
                    print("o cliente encontrado: " + client)
                    self.__ip = client
                    print(self.__ip)
                    print("Connection successfully")
                    return self.__ip
                else:
                    print("Connection failed 1")
                    self.__s.close()
            except:
                print("Connection failed 2")

    def getIp(self):
        return self.__ip



    
