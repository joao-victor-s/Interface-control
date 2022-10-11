import socket
import time
from Control_Interface.controlInterface import controlInterface



def main():
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
        elem.setVoltage(110)
        elem.start()
        print("nhr10 ip: ",elem.getIp())
        print("nhr 10 array: ", elem.getVoltageArray())
  
        

    for elem in nhr30:
        elem.setCurrent(10)
        elem.start()
        print("nhr30 ip: ",elem.getIp())
        print("nhr 30 array: ", elem.getCurrentArray())
        


    time.sleep(3)

    for elem in nhr10:
        elem.close()
    for elem in nhr30:
        elem.close()

if __name__ == '__main__':
    main()
