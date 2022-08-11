import socket
import time
from Control_Interface.controlInterface import controlInterface



def main():
    interface = controlInterface()

    interface.__init__()
    print(interface.getListIp())
    interface.newNhr("9410")
    #interface.newNhr("9430")
    #interface.newNhr("9430")

    nhr10 = []
    nhr30 = []
    nhr10 = interface.getNhr9410()
    nhr30 = interface.getNhr9430()


    for elem in nhr10:
            print("nhr10 ip: ",elem.getIp())
            print("nhr10 max current: ", elem.instrumentCapCurrent())
            print("nhr10 max current range: ", elem.instrumentCapCurrentRange())
            print("nhr10 max freq range: ", elem.instrumentCapFreqRange())
            print("nhr10 max power range: ", elem.instrumentCapPowerMax())
            print("nhr10 max voltage range: ", elem.instrumentCapVoltageMaxMin())

        


    for elem in nhr30:
        print("nhr30 ip: ",elem.getIp())


    time.sleep(3)

    for elem in nhr10:
        elem.close()
    for elem in nhr30:
        elem.close()

if __name__ == '__main__':
    main()
