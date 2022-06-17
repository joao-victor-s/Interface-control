import random
import socket


class NHR9400:
    
    def __init__(self, name):
        self.__id = random.randrange(100, 300, 2)
        self.__name = name

    
    def start(void):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.timeout(1)
        