from PyQt5.QtWidgets import QApplication, QMainWindow
import serial
import serial.tools.list_ports
from PyQt5.QtCore import QThread, pyqtSignal
from FUNCTIONS import *
import enum


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
        UNLOCKED    = 3

    class BUTTONSTATE(enum.Enum):
        PRESS           = 0,
        RELEASE         = 1,
        HOLD            = 2


    
    rx_signal:pyqtSignal = pyqtSignal()
    notConn_signal:pyqtSignal = pyqtSignal()
    conn_signal:pyqtSignal = pyqtSignal()

    state:NANOSTATE = NANOSTATE.DISCONNECTED

    DOOR_STATE:DOORSTATE = DOORSTATE.OPEN               # Hall State
    LATCH_STATE:DOORSTATE = DOORSTATE.UNLOCKED
    BUTTON_STATE:BUTTONSTATE = BUTTONSTATE.RELEASE
    PIR_STATE:bool = False

    pir_timer = QTimer()
    
    
    def __init__(self, port, baudrate):
        super().__init__()

        self.serial = serial.Serial()
        
        try:
            self.serial = serial.Serial(port, baudrate, timeout=0)
        except serial.SerialException as e:
            self.state = self.NANOSTATE.DISCONNECTED

    def run(self):
        while True:

            if self.state == self.NANOSTATE.DISCONNECTED:
                if self.serial.isOpen():
                    self.conn_signal.emit()  # Emit signal when connection is established
                    self.state = self.NANOSTATE.CONNECTED

            elif self.state == self.NANOSTATE.CONNECTED:
                if not self.serial.isOpen():
                    self.notConn_signal.emit()  # Emit signal if connection is lost
                    self.state = self.NANOSTATE.DISCONNECTED
                else:
                    self.state = self.NANOSTATE.WAIT_RX  # Proceed to WAIT_RX state

            elif self.state == self.NANOSTATE.WAIT_RX:
                if not self.serial.isOpen():
                    self.notConn_signal.emit()  # Emit signal if connection is lost
                    self.state = self.NANOSTATE.DISCONNECTED
                else:
                    data = self.serial.readline()
                    if data:
                        self.state = self.NANOSTATE.RECIEVING  # Update state to RECEIVING
                        self.convertRxData( int(data.decode('utf-8')) )
                        self.state = self.NANOSTATE.WAIT_RX  # Revert state back to WAIT_RX after handling data

    def convertRxData(self, data:int):

        if data & 0b1:     # Hall Idle
            self.DOOR_STATE = self.DOORSTATE.OPEN
            
        if data & 0b10:    # Hall Detect
            self.DOOR_STATE = self.DOORSTATE.CLOSE

        if data & 0b100:   # Button Hold  
            self.BUTTON_STATE = self.BUTTONSTATE.HOLD

        if data & 0b1000:  # Button Release
            self.BUTTON_STATE = self.BUTTONSTATE.RELEASE

        if data & 0b10000: # Button Press
            self.BUTTON_STATE = self.BUTTONSTATE.PRESS

        if data & 0b100000: # PIR Trigger
            self.PIR_STATE = True

        self.rx_signal.emit()

            

        

        

                    

