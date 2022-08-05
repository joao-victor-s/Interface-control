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


for elem in nhr10:
    print("nhr10 ip: ",elem.getIp())
    
    elem.setVoltage(220)
    elem.setPower(5)
    elem.start()
    
    print("voltage:",elem.getVoltage())
    print("current:", elem.getCurrent())
    print("Power:", elem.getPower())
    print(elem.checkErrors())

for elem in nhr30:
    print("nhr30 ip: ",elem.getIp())
    elem.setCurrent(30)
    elem.start()
    print("voltage:",elem.getVoltage())
    print("current:", elem.getCurrent())
    print("Power:", elem.getPower())


time.sleep(20)

for elem in nhr10:
    elem.close()
for elem in nhr30:
    elem.close()