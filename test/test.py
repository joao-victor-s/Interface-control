#Arquivo para teste em geral
import socket
from scapy.all import ARP, Ether, srp, arping
import socket
import time
start = time.time()

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.settimeout(1)

s.connect(("192.168.0.2",5025))

s.send("SYST:RWL\n".encode()) #Command to activate remote control and locking the touchscreen
s.send("*IDN?\r\n".encode())
msg = s.recv(1024)
print(msg)


s.send("SOUR:OUTP:ON 1\n".encode())
s.send("INIT\n".encode())
s.send("SOUR:VOLT: 110\r\n".encode())



s.send("SYST:ERR?\n".encode())
msg = s.recv(1024)
print(msg)

time.sleep(5)
s.send("SOUR:OUTP:ON 0\n".encode())
s.send("SYST:LOC\n".encode())

s.close()