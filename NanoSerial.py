from PyQt5.QtWidgets import QApplication, QMainWindow
import serial
import serial.tools.list_ports
from PyQt5.QtCore import QThread, pyqtSignal
from FUNCTIONS import *
import enum
import glob
from typing import List
import sys


class NANO(QThread):

    class NANOSTATE(enum.Enum):
        DISCONNECTED    = 0,
        CONNECTED       = 1,
        WAIT_RX         = 2,
        RECIEVING       = 3

    class DOORSTATE(enum.Enum): # Hall Effect and Latch Feedback
        OPEN        = 0,
        CLOSE       = 1,
        LOCKED      = 2,
        UNLOCKED    = 3,
        JAMMED      = 4,
        LOCKING     = 5,
        UNLOCKING   = 6

    class BUTTONSTATE(enum.Enum):
        PRESS           = 0,
        RELEASE         = 1,
        HOLD            = 2


    
    rx_signal:pyqtSignal = pyqtSignal(int)
    door_signal:pyqtSignal = pyqtSignal(DOORSTATE)
    button_signal:pyqtSignal = pyqtSignal(BUTTONSTATE)
    pir_signal:pyqtSignal = pyqtSignal()
    nano_signal:pyqtSignal = pyqtSignal(NANOSTATE)

    state:NANOSTATE = NANOSTATE.DISCONNECTED

    DOOR_STATE:DOORSTATE = DOORSTATE.OPEN               # Hall State
    LATCH_STATE:DOORSTATE = DOORSTATE.UNLOCKED
    BUTTON_STATE:BUTTONSTATE = BUTTONSTATE.RELEASE
    PIR_STATE:bool = False

    pir_timer = QTimer()
    port = None
    baudrate = None

    debug:bool = False
    
    
    def __init__(self, port, baudrate, debug = True):

        super().__init__()

        self.serial = serial.Serial()
        self.debug = debug
        self.port = port
        self.baudrate = baudrate
        
        self.state = self.NANOSTATE.DISCONNECTED
        

    def run(self):
        while True:

            #######################################################################
            if self.state == self.NANOSTATE.DISCONNECTED:

                ports:List(str) = self.list_serial_ports()

                for __port in ports:
                    port:str = __port
                    if port.__contains__("USB"):
                        try:
                            self.serial = serial.Serial(port, 9600, timeout=1)
                            if self.serial.isOpen():
                                self.nano_signal.emit(self.NANOSTATE.CONNECTED)  # Emit signal when connection is established
                                self.state = self.NANOSTATE.CONNECTED
                                if self.debug: print("Serial - Connected")
                                if self.debug: print(f"Port - {port}")
                                break
                        except serial.SerialException as e:
                            pass
                    

            ######################################################################
            elif self.state == self.NANOSTATE.CONNECTED:

                if not self.serial.isOpen():
                    self.nano_signal.emit(self.NANOSTATE.DISCONNECTED)  # Emit signal if connection is lost
                    self.state = self.NANOSTATE.DISCONNECTED
                    if self.debug: print("Serial - Disconnected")
                else:
                    self.nano_signal.emit(self.NANOSTATE.WAIT_RX)
                    self.state = self.NANOSTATE.WAIT_RX  # Proceed to WAIT_RX state
                    if self.debug: print("Serial - Wait RX")

            ######################################################################
            elif self.state == self.NANOSTATE.WAIT_RX:
                if not self.serial.isOpen():
                    self.notConn_signal.emit()  # Emit signal if connection is lost
                    self.nano_signal.emit(self.NANOSTATE.DISCONNECTED)
                    self.state = self.NANOSTATE.DISCONNECTED
                    if self.debug: print("Serial - Disconnected")
                else:
                    
                    try:
                        data = self.serial.readline()
                        if data:
                            self.nano_signal.emit(self.NANOSTATE.RECIEVING)
                            self.state = self.NANOSTATE.RECIEVING  # Update state to RECEIVING
                            self.convertRxData( int(data.decode('utf-8')) )
                            self.nano_signal.emit(self.NANOSTATE.WAIT_RX)
                            self.state = self.NANOSTATE.WAIT_RX  # Revert state back to WAIT_RX after handling data

                    except serial.SerialException as e:
                        self.nano_signal.emit(self.NANOSTATE.DISCONNECTED)
                        self.state = self.NANOSTATE.DISCONNECTED
                        if self.debug: print("Serial - Disconnected")


                    
    def convertRxData(self, data:int):

        print(data)

        data &= 0b11111111111


        self.rx_signal.emit( data )


    def list_serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of available serial ports
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # This is to exclude your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        return ports
    
    def DOOR( self, state: DOORSTATE ):

        if state == self.DOORSTATE.LOCKED:
            self.serial.write( int(0b00010001).to_bytes(1) )
        elif state == self.DOORSTATE.UNLOCKED:
            self.serial.write( int(0b00010000).to_bytes(1) )
        else:
            return
        
    def resetJammed(self):
        self.serial.write( int(0b00010010).to_bytes(1) )

    


    

    


            

        

        

                    

