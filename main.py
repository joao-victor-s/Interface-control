import socket
import time
from Control_Interface.controlInterface import controlInterface

interface = controlInterface()

interface.__init__()
print(interface.getListIp())
interface.newNhr("9410")
interface.newNhr("9430")
#interface.newNhr("9430")

nhr10 = []
nhr30 = []
nhr10 = interface.getNhr9410()
nhr30 = interface.getNhr9430()

print(nhr10)
print(nhr30)


for elem in nhr10:
    print("nhr10 ip: ",elem.getIp())
    elem.setVoltage(220)
    time.sleep(1)
    elem.setPower(0.7)
    print(elem.checkErrors())
    print("voltage:",elem.getVoltage())
    print("current:", elem.getCurrent())
    print("Power:", elem.getPower())
    elem.close()

for elem in nhr30:
    print("nhr30 ip: ",elem.getIp())
    elem.setCurrent(30)
    print("voltage:",elem.getVoltage())
    print("current:", elem.getCurrent())
    print("Power:", elem.getPower())
    elem.close()