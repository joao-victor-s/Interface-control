from Control_Interface.controlInterface import controlInterface
from Utility.IPFinder import IPFinder

interface = controlInterface()
interface.__init__()
interface.newNhr9410()
interface.newNhr9430()
#interface.newNhr9430()
nhr10 = []
nhr30 = []
nhr10 = interface.getNhr9410()
nhr30 = interface.getNhr9430()

print(nhr10)
print(nhr30)