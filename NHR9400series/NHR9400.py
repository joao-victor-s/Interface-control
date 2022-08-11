from abc import abstractmethod
import socket
from UtilitiesRei.refineOutput import refineOutput


class NHR9400():
    
    def __init__(self, name):
        self.__name = name
        self.__s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__s.settimeout(1)
        self.__ip = ""

################################# Configurations ######################################################
    #Default start: Enable all instruments and close output relays and starts an aperture measurement on all channels which will run for the time specified by the last received SENSe:SWEep:APERture instrument command
    #!!!!!! upgrade this function later
    def start(self):
        self.__s.send("SOUR:OUTP:ON 1\n".encode())
        self.__s.send("INIT\n".encode())

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

    def getS(self):
        return self.__s

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
        value = self.__s.recv(1024)
        return self.receiveString(value)

    def close(self):
        self.__s.send("SOUR:OUTP:ON 0\n".encode())
        self.__s.send("ABOR\n".encode())
        self.__s.send("SYST:LOC\n".encode())
        print(self.checkErrors())
        self.__s.close()
    # Controle do relé de saída do hardware (LIGAR OU DESLIGAR)
    # 0 OFF - Instrumento desabilitado
    # 1 ON - Instrumento habilitado
    def enableOutput(self, value):
        if value == 0 or value == 1:
            self.__s.send(("SOUR:OUTP:ON "+ str(value) + "\n").encode())
        else:
            print("INVALID INPUT")
################################# System command #####################################################
    #Command places the touch panel (if present) in local control mode. All front panel keys are returned to a functional state.
    def systLocal(self):
        self.__s.send("SYST:LOC\n".encode())
    #Command or receipt of an external SCPI command places the touch panel in a non-locked remote mode.
    def systRemote(self):
        self.__s.send("SYST:REM\n".encode())
    #Query returns the SCPI version number to which the module complies. The value is of the form YYYY.V, where YYYY is the year and V is the revision number for that year.    
    def systVersion(self):
        self.__s.send("SYST:VER\n".encode())
    #Command specifies the interval (Seconds) in which a command must be received. Query returns the programmed watchdog interval (Seconds).
    def systWatchdogInterval(self, interval):
        if interval < 0: return -1
        self.__s.send(("SYST:WATC:INT" + str(interval) +"\n").encode())

    #Command determines the type communication required to reset the watchdog timer. Query returns the type of communication required to reset the watchdog timer.
    def systWatchdogRobust(self, bool):
        if bool != 0 or bool != 1: return -1
        self.__s.send(("SYST:WATC:ROB" + str(bool) +"\n").encode())
    
    #Command resets watchdog timer
    def systWatchdogService(self):
        self.__s.send(("SYST:WATC:SERV\n").encode())

################################# Digital Subsystem ############################

    #Query returns the current state of the general purpose digital input port on the specified module.
    def digitalInput(self):
        self.__s.send(("DIG:INP\n").encode())
    #Query returns the number of general purpose digital inputs (expressed as number of bits).
    def digitalInputCount(self):
        self.__s.send(("DIG:INP:COUN\n").encode())
    #Command sets the state of the general purpose digital output port on the specified module. Query returns the last programmed state of the general purpose digital output
    def digitalOutput(self):
        self.__s.send(("DIG:OUT\n").encode())
    #Query returns the number of general purpose digital outputs (expressed as number of bits).
    def digitalInputCount(self):
        self.__s.send(("DIG:OUT:COUN\n").encode())
################################# Instrument Capabilities - System Information Queries ##############################

# Query returns the number of output channels detected by the hardware.
    def instrumentSystemChanels(self):
        self.__s.send(("INST:CAP:SYST:CHAN?\r\n").encode())
        value = self.__s.recv(1024)
        return self.receiveString(value)
    
# Query returns the number of chassis detected (Master + Auxiliaries)
    def instrumentSystemChassis(self):
        self.__s.send(("INST:CAP:SYST:CHAS?\n").encode()) 
        value = self.__s.recv(1024)
        return self.receiveFloat(value)

#Query returns the maximum number of commands which can be stored in a macro
    def instrumentSystemMacros(self):
        self.__s.send(("INST:CAP:MACR:COMM:MAX?\n").encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)

#Query returns the maximum delay time allowed for MACRo:WAIT[:TIME] within a single macro step.
    def instrumentSystemMacroDelay(self):
        self.__s.send(("INST:CAP:MACR:DEL:MAX?\n").encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)

#Query returns the default Regulation Gain setting set value used by the hardware.
    def instrumentSystemRGainNominal(self):
        self.__s.send(("INST:CAP:RGA:NOM?\n").encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)

#Query returns the maximum Regulation Gain setting set value used by the hardware.
    def instrumentSystemRGainMax(self):
        self.__s.send(("INST:CAP:RGA:MAX?\n").encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)

#Query returns the maximum trip time (seconds) for a safety limit settings
    def instrumentSystemTripMax(self):
        self.__s.send(("INST:CAP:TRIP:MAX?\n").encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)

################################# Instrument Capabilities - Measurement Capabilities Queries ############################## 
#Query returns a list with the absolute maximum and minimum measurement aperture setting for the module.
    def instrumentSystemApertureRange(self):
        range = []
        self.__s.send(("INST:CAP:APER:MIN?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        self.__s.send(("INST:CAP:APER:MAX?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        
        return range

#Query returns the absolute peak current measurement capability for instrument selected.
    def instrumentSystemCurrent(self):
        range = []
        self.__s.send(("INST:CAP:CURR:MEAS:MIN?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        self.__s.send(("INST:CAP:CURR:MEAS:MAX?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        
        return range
#Query returns maximum (minimum) peak current measurement for the selected instrument & range
    def instrumentSystemCurrentRange(self):
        range = []
        self.__s.send(("INST:CAP:CURR:MEAS:RANG:MIN?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        self.__s.send(("INST:CAP:CURR:MEAS:RANG:MAX?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        
        return range
#Query returns the waveform digitizer’s maximum (minimum) sample frequency in Hz.
    def instrumentSystemFreq(self):
        range = []
        self.__s.send(("INST:CAP:SAMP:FREQ:MIN?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        self.__s.send(("INST:CAP:SAMP:FREQ:MAX?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        
        return range

#Query returns the waveform digitizer’s maximum sample memory depth
    def instrumentSamplePoints(self):
        self.__s.send(("INST:CAP:SAMPl:POIN:MAX?\n").encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)

#Query returns the absolute peak voltage measurement capability for instrument selected.
#For AC (1φ) & DC outputs: Query response is expressed as line-neutral.
#For AC multi-φ outputs: Query response is expressed as line-line equivalent value.
    def instrumentSystemVoltage(self):
        range = []
        self.__s.send(("INST:CAP:VOLT:MEAS:MIN?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        self.__s.send(("INST:CAP:VOLT:MEAS:MAX?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        
        return range
    
    def instrumentSystemVoltagePhase(self, phase):
        if phase == 1:
            msg = "INST:CAP:VOLT:APH:"
        elif phase == 2:
            msg = "INST:CAP:VOLT:BPH:"
        elif phase == 3:
            msg = "INST:CAP:VOLT:CPH:"
        else:
            return -1
        range = []
        self.__s.send((msg + "MEAS:MIN?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        self.__s.send((msg + "MEAS:MAX?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        
        return range
#Query returns maximum (minimum) peak voltage measurement for the selected instrument & range
    def instrumentSystemVoltageRange(self):
        range = []
        self.__s.send(("INST:CAP:VOLT:MEAS:RANG:MIN?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        self.__s.send(("INST:CAP:VOLT:MEAS:RANG:MAX?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        
        return range

    def instrumentSystemVoltageRangePhase(self, phase):
        if phase == 1:
            msg = "INST:CAP:VOLT:APH:"
        elif phase == 2:
            msg = "INST:CAP:VOLT:BPH:"
        elif phase == 3:
            msg = "INST:CAP:VOLT:CPH:"
        else:
            return -1
        range = []
        self.__s.send((msg + "MEAS:RANG:MIN?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        self.__s.send((msg + "MEAS:RANG:MAX?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        
        return range

################################# Instrument Capabilities - Setting Capabilities Queries ##############################

# Query returns the absolute maximum current (ARMS or ADC) output capability for instrument selected.
    def instrumentCapCurrent(self):
        self.__s.send(("INST:CAP:CURR:MAX?\r\n").encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)
#Query returns the maximum current (ARMS or ADC) set-point value for selected instrument & range
    def instrumentCapCurrentRange(self):
        self.__s.send(("INST:CAP:CURR:RANG:MAX?\n").encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)

#Query returns a list of maximum or minimum current (ARMS or ADC) ranges for the selected instrument.
    def instrumentCapCurrentRangeList(self):
        range = []
        self.__s.send(("INST:CAP:CURR:RANG:LIST:MIN?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveString(value))
        self.__s.send(("INST:CAP:CURR:RANG:LIST:MAX?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveString(value))
        
        return range

#Query returns the maximum (minimum) allowable operating frequency.
    def instrumentCapFreqRange(self):
        range = []
        self.__s.send((":INST:CAP:FREQ:RANG:MIN?\r\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        self.__s.send(("INST:CAP:FREQ:RANG:MAX?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        
        return range

#Query returns the absolute maximum true power (Watts) setting value for the instrument selected.
    def instrumentCapPowerMax(self):
        self.__s.send(("INST:CAP:POW:ALL:MAX?\n").encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)
#  for each phase
    def instrumentCapPowerMaxPhase(self, phase):
        if phase == 1:
            msg = "INST:CAP:POW:APH:"
        elif phase == 2:
            msg = "INST:CAP:POW:BPH:"
        elif phase == 3:
            msg = "INST:CAP:POW:CPH:"
        else:
            return -1
        self.__s.send((msg + "MAX?\n").encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)
#These queries will retrieve the minimum (smallest positive) and maximum (largest positive) positive resistance setting for the Module. For example, the minimum = 1.5 and maximum = 1000.
    def instrmentCapResistencePos(self):
        self.__s.send(("INST:CAP:RES:POS:MIN?\r\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        self.__s.send(("INST:CAP:RES:POS:MAX?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        
        return range
    
    def instrmentCapResistencenNeg(self):
        self.__s.send(("INST:CAP:RES:NEG:MIN?\r\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        self.__s.send(("INST:CAP:RES:NEG:MAX?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        
        return range
#Query returns the absolute maximum voltage (VRMS or VDC) output capability for instrument selected.
    def instrumentCapVoltageMaxMin(self):
        range = []
        self.__s.send(("INST:CAP:VOLT:ALL:MIN?\r\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        self.__s.send(("INST:CAP:VOLT:ALL:MAX?\n").encode())
        value = self.__s.recv(1024)
        range.append(self.receiveFloat(value))
        
        return range
################################# Setters and Getters ################################################

#set limit voltage of all phases
    def setVoltage(self,voltage):
        if voltage < 0:
            return -1
        self.__s.send(("SOUR:VOLT: " + str(voltage) + "\n").encode())
    #Functions that sets the limits voltage on one phase (A, B or C)
    def setVoltageA(self,voltage):
        if voltage < 0:
            return -1
        self.__s.send(("SOUR:VOLT:APH " + str(voltage) + "\n").encode())

    def setVoltageB(self,voltage):
        if voltage < 0:
            return -1
        self.__s.send(("SOUR:VOLT:BPHase " + str(voltage) + "\n").encode())

    def setVoltageC(self,voltage):
        if voltage < 0:
            return -1
        self.__s.send(("SOUR:VOLT:CPHase " + str(voltage) + "\n").encode())

    #Command establishes the True Power limit (W) as a positive value for the selected instrument.
    def setPower(self, pow):
        if pow < 0:
            return -1
        self.__s.send(("SOUR:POW: " + str(pow) + "\n").encode())
    #Individual command for one phase
    def setPowerA(self, pow):
        if pow < 0:
            return -1
        self.__s.send(("SOUR:POW:APHase " + str(pow) + "\n").encode())
    def setPowerB(self, pow):
        if pow < 0:
            return -1
        self.__s.send(("SOUR:POW:BPHase " + str(pow) + "\n").encode())
    def setPowerC(self, pow):
        if pow < 0:
            return -1
        self.__s.send(("SOUR:POW:CPHase " + str(pow) + "\n").encode())
    #Command establishes the operating frequency for the selected instrument.
    def setFreq(self, freq):
        if freq < 0:
            return -1
        self.__s.send(("SOUR:FREQ " + str(freq) + "\n").encode())
    #!!!! Doesnt work!!!!
    def getFreq(self):
        self.__s.send("FETC:FREQ\n".encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)
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
        self.__s.send("FETC:CURR?\n".encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)
    #fetch individual value of current of one channel
    def getCurrentA(self):
        self.__s.send("FETC:CURR:APHase?\n".encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)

    def getCurrentB(self):
        self.__s.send("FETC:CURR:BPHase?\n".encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)

    def getCurrentC(self):
        self.__s.send("FETC:CURR:CPHase?\n".encode())
        value = self.__s.recv(1024)
        return self.receiveFloat(value)
    
