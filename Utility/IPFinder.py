import socket
from threading import local
from scapy.all import ARP, Ether, srp


class IPFinder:
    
    #uses socket and scapy to scan the entire local network and returns all the IPs adresses of the devices connects in this networok
    def getAllIp():
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(("10.255.255.255",1))
        local_ip = s.getsockname()[0]
        
        local_ip = local_ip[:-1] + "/24"
        print(local_ip)
        print(type(local_ip))
        arp = ARP(pdst=local_ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp

        result = srp(packet, timeout=1, verbose=0)[0]
        clients = []
        for sent, received in result:
            clients.append({"ip": received.psrc})
        for client in clients:
            print(client['ip'])