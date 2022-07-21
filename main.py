from Control_Interface.controlInterface import controlInterface


interface = controlInterface()

interface.__init__()
print(interface.getListIp())
interface.newNhr9410()
interface.newNhr9430()
#interface.newNhr9430()
nhr10 = []
nhr30 = []
nhr10 = interface.getNhr9410()
nhr30 = interface.getNhr9430()

print(nhr10)
print(nhr30)

for elem in nhr10:
    print(elem.getIp())
    elem.close()
for elem in nhr30:
    elem.close()