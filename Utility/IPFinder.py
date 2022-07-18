import socket
from threading import local
from scapy.all import ARP, Ether, srp


class IPFinder:



    def __init__(self):
        self.__clients = self.getAllIp()
    #uses socket and scapy to scan the entire local network and returns all the IPs adresses of the devices connects in this networok
    def __getAllIp(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(("10.255.255.255",1))
        local_ip = s.getsockname()[0]
        
        splited = local_ip.split('.')
        splited = local_ip.split('.')
        splited.pop()
        splited.append("1/24")
        local_ip = ".".join(splited)

        arp = ARP(pdst=local_ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp

        result = srp(packet, timeout=1, verbose=0)[0]
        clients = []
        for sent, received in result:
            clients.append({"ip": received.psrc})
        self.__clients = clients

    def deteleIp(self, ip):
        self.__clients.remove(ip)

    def getList(self):
        return self.__clients