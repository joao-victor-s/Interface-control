from abc import abstractmethod
import socket
from UtilitiesRei.refineOutput import refineOutput


class NHR9400:
    
    def __init__(self, name):
        self.__name = name
        self.__s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__s.settimeout(1)
        self.__ip = ""

################################# Configurations ######################################################
    def locateIp(self, clients = []):
        for client in clients:
            try:

                self.__s  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.__s.connect((client, 5025))
                self.__s.send("SYST:RWL\n".encode()) #Command to activate remote control and locking the touchscreen
                self.__s.send("*IDN?\n".encode())
                msg = self.__s.recv(1024)
                recv = self.receiveString(msg)
                id = "NH Research," + str(self.__name)
                if recv.find(id) != -1: #if find this subtring 
                    self.__ip = client
                    print(self.__ip)
                    print("Connection successfully")
                    break
                else:
                    self.__s.close()
            except:
                print("Connection failed 2")

    def getIp(self):
        return self.__ip

    #chose a mode with the instrument will run, check the manual to see all modes.
    def configMode(self, mode):
        if mode < 0 and mode > 16:
            print("INVALID INPUT")
        else:
            self.__s.send(("CONF:HW:MODE " + str(mode) + "\n").encode())
            self.checkErrors()
            self.validMode()
    #check if the mode is valid for the current hardware
    def validMode(self):
        self.__s.send("CONF:HW:MODE:VAL".encode())
        print(self.receiveString())

    #Command configures if [SOURCe:]<Function> commands are immediately or phase-angle controlled Query returns the synchronous operating mode
    def instrumentSync(self, value):
        if value == 0 or value == 1:
            self.__s.send(("CONF:INST:SYNC "+ str(value) + "\n").encode())
        else:
            print("INVALID INPUT")

    #The 9400 will contain one (1), two (2), or three (3) logical instruments depending on the CONFigure:HW:MODE selected. Unless otherwise noted in a specific command, Any command or queries with an INSTRUMENT scope will be processed by the last instrument selected by either an INSTrument:NSELect or an INSTrument:SELect.
    def instrumentNselect(self, value):
        if value < 1 or value > 3:
            print("INVALID INPUT")
        else:
                self.__s.send(("INST:NSEL " + str(value) + "\n").encode())
        self.checkErrors()

    #Command selects an instrument by its alias name created with INSTrument:DEFine[:NAME]. Query returns the current selected logical instrument alias name.
    #check this command, maybe something wrong
    def instrumentSelect(self):
        self.__s.send("INST:SEL".encode())
        self.checkErrors()

    #Command assigns an alias name allowing selection of the instrument using INSTrument:SELect <name> Query returns the alias name assigned to a specific output channel.

    def instrumentDefName(self, name, num):
        self.instrumentNselect(num)
        self.__s.send(("INST:DEF:" + str(name) + "\n").encode())
        self.checkErrors()
    #Command disassociates an <identifier> alias from the logical instrument number.
    #After the command executes, the default identifier is re-associated with the instrument number.
    #The default identifier cannot be deleted.
    def instDelName(self, name):
        self.__s.send(("INST:DEL:" + str(name) + "\n").encode())
        self.checkErrors()
    #Query returns the <identifier> alias for the requested instrument number.
    #If no instrument number is provided, the <identifier> of the selected instrument is returned.
    def instrumentName(self, num):
        if num < 1 or num > 3:
            print("INVALID INPUT")
        else:
                self.__s.send(("INST:NAME " + str(num) + "\n").encode())
        self.checkErrors()
    #Function that receives messages back and transform it in a string
    def receiveString(self,recv):
        recv = refineOutput().byteToString(recv)
        return recv

    #Function that receives messages back and transform it in a float
    def receiveFloat(self, msg):
        msg = refineOutput().byteToFloat(msg)
        return msg

    def identify(self):
        self.__s.send("*IDN?\n".encode())
        return self.receive()
    #Function to see if exist any error in the carry
    def checkErrors(self):
        self.__s.send("SYST:ERR?\n".encode())
        self.__s.timeout(5)
        return self.receive()

    def close(self):
        self.__s.send("SYST:LOC\n".encode())
        self.__s.close()
    # Controle do relé de saída do hardware (LIGAR OU DESLIGAR)
    # 0 OFF - Instrumento desabilitado
    # 1 ON - Instrumento habilitado
    def enableOutput(self, value):
        if value == 0 or value == 1:
            self.__s.send(("SOUR:OUTP:ON "+ str(value) + "\n").encode())
        else:
            print("INVALID INPUT")
################################# Setters and Getters ################################################
    #set limit voltage of all phases
    def setVoltage(self,voltage):
        self.__s.send(("SOUR:VOLT " + str(voltage) + "\n").encode())
    #Functions that sets the limits voltage on one phase (A, B or C)
    def setVoltageA(self,voltage):
        self.__s.send(("SOUR:VOLT:APH " + str(voltage) + "\n").encode())

    def setVoltageB(self,voltage):
        self.__s.send(("SOUR:VOLT:BPHase " + str(voltage) + "\n").encode())

    def setVoltageC(self,voltage):
        self.__s.send(("SOUR:VOLT:CPHase " + str(voltage) + "\n").encode())

    #Command establishes the True Power limit (W) as a positive value for the selected instrument.
    def setPower(self, pow):
        self.__s.send(("SOUR:POW " + str(pow) + "\n").encode())
    #Individual command for one phase
    def setPowerA(self, pow):
        self.__s.send(("SOUR:POW:APHase " + str(pow) + "\n").encode())
    def setPowerB(self, pow):
        self.__s.send(("SOUR:POW:BPHase " + str(pow) + "\n").encode())
    def setPowerC(self, pow):
        self.__s.send(("SOUR:POW:CPHase " + str(pow) + "\n").encode())
    #Command establishes the operating frequency for the selected instrument.
    def setFreq(self, freq):
        self.__s.send(("SOUR:POW " + str(freq) + "\n").encode())
    #Fetch the average voltage of all channels
    def getVoltage(self):
        self.__s.send("FETC:VOLT?\n".encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)
    #fetch individual value of voltage of one channel
    def getVoltageA(self):
        self.__s.send("FETC:VOLT:APHase?\n".encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)
    def getVoltageB(self):
        self.__s.send("FETC:VOLT:BPHase?\n".encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)
    def getVoltageC(self):
        self.__s.send("FETC:VOLT:CPHase?\n".encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)
        
    #Fetch the average power of all channels
    def getPower(self):
        self.__s.send("FETC:POW?\n".encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)
    #fetch individual value of Power of one channel
    def getPowerA(self):
        self.__s.send("FETC:POW:APHase?\n".encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)
    def getPowerB(self):
        self.__s.send("FETC:POW:BPHase?\n".encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)
        
    def getPowerC(self):
        self.__s.send("FETC:POW:CPHase?\n".encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)

        #Fetch the average current of all channels
    def getCurrent(self):
        value = self.__s.send("FETC:CURR?\n".encode())
        return self.receiveFloat(value)
    #fetch individual value of current of one channel
    def getCurrentA(self):
        value = self.__s.send("FETC:CURR:APHase?\n".encode())
        return self.receiveFloat(value)
    def getCurrentB(self):
        value = self.__s.send("FETC:CURR:BPHase?\n".encode())
        return self.receiveFloat(value)
    def getCurrentC(self):
        value = self.__s.send("FETC:CURR:CPHase?\n".encode())
        return self.receiveFloat(value)
    
