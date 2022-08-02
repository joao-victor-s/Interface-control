#Arquivo para teste em geral
import socket
from scapy.all import ARP, Ether, srp, arping
import socket
import time
start = time.time()

def getAllIp():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("10.255.255.255",1))
    local_ip = s.getsockname()[0]
    print(local_ip)
    local_ip = local_ip[:-3] + "1/24"
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
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.settimeout(1)
try: 
    s.connect(("192.168.15.10", 5025))
except:
    print("conexão falhou")
print (time.time() - start)
