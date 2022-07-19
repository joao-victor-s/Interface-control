from Control_Interface.controlInterface import controlInterface


interface = controlInterface

interface.newNhr9410()
interface.newNhr9430()
#interface.newNhr9430()
nhr10 = []
nhr30 = []
nhr10 = interface.getNhr9410()
nhr30 = interface.getNhr9430()

print(nhr10)
print(nhr30)

nhr10[0].getIp
nhr30[0].getIp
