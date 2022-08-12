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
        print("nhr10 watch dog interval: ", elem.systWatchdogInterval(0))
        print("nhr10 ip: ",elem.getIp())
        print("nhr10 max current: ", elem.instrumentCapCurrent())
        print("nhr10 current range: ", elem.instrumentCapCurrentRange())
        print("nhr10 freq range: ", elem.instrumentCapFreqRange())
        print("nhr10 power range: ", elem.instrumentCapPowerMax())
        print("nhr10 voltage range: ", elem.instrumentCapVoltageMaxMin())
        

    for elem in nhr30:
        print("nhr30 ip: ",elem.getIp())
        print("nhr10 watch dog interval: ", elem.systWatchdogInterval(5))
        print("nhr30 max current: ", elem.instrumentCapCurrent())
        print("nhr30 current range: ", elem.instrumentCapCurrentRange())
        print("nhr30 freq range: ", elem.instrumentCapFreqRange())
        print("nhr30 power range: ", elem.instrumentCapPowerMax())
        print("nhr30 voltage range: ", elem.instrumentCapVoltageMaxMin())
        print("nhr30  range: ", elem.instrumentCapResistenceRL())
        


    time.sleep(3)

    for elem in nhr10:
        elem.close()
    for elem in nhr30:
        elem.close()

if __name__ == '__main__':
    main()
