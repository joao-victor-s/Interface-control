import socket
import dec

class mug():
    def __init__(self,name):
        self.__name: name
        self.__s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__s.settimeout(1)
    
    def decode(self, recv):
        recv = dec.dec().rewrite(recv)
        return recv
    
    def getS(self):
        return self.__s