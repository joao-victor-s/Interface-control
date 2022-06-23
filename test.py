#Arquivo para teste em geral
import socket
from scapy.all import ARP, Ether, srp, arping
import time
start = time.time()

def getAllIp():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("10.255.255.255",1))
    local_ip = s.getsockname()[0]
    print(local_ip)
    local_ip = local_ip[:-1] + "/24"
    print(local_ip)
    print(type(local_ip))
    arp = ARP(pdst=local_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result= srp(packet, timeout=3,retry = 1, verbose = 0)[0]
    clients = []
    for sent, received in result:
        clients.append(received.psrc)
    
    for client in clients:
        print(client)

getAllIp()
print (time.time() - start)