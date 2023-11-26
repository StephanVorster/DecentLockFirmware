import sys
from Window import *
from NanoSerial import *
from nfc_handler import *

class MainSystem():

    timer:QTimer = QTimer()


    def __init__(self, UI:UI_MAIN):

        self.UI = UI

        self.nano = NANO( '/dev/ttyUSB0', 9600 )
        self.nano.rx_signal.connect( self.HANDLER_NANO_RX )
        self.nano.start()

        
        self.timer.setSingleShot(True)
        print("Creaed NFC Object")
        self.nfc = nfc_auth_handler(debug=True)

        self.START_UP()

    def HANDLER_NANO_RX(self):
        pass

    def START_UP(self):
        print( "Start UP" )
        self.UI.INIT_LOADING()
        self.timer.timeout.connect( self.STARTUP_IDLE )
        self.timer.start(1000)
    
    def STARTUP_IDLE(self):
        self.UI.INITLOADING_LOCKEDSCREEN()
        self.nfc.setStateReady(True)
        def handler( state:bool ):
            print(state)
            if state: self.ONLINEMODE_SUCCESS()
            else: self.ONLINEMODE_FAILED()

        self.nfc.auth_signal.connect( handler )
        print("Attempting Thread Start")
        self.nfc.start()
        print( "Idle" )

    def ONLINEMODE_WAIT(self, x):
        print("Online Wait")
        self.UI.ONLINE_MODE()
        
        

        print( "Load" )
        

    def ONLINEMODE_SUCCESS(self):
        self.UI.UNLOCKED_SCREEN()
        print( "Unlock" )

    def ONLINEMODE_FAILED(self):
        self.UI.loading.SET_EXTCB_EXIT( self.UI.locked.ENTRANCE )
        self.UI.loading.EXIT()
        print( "Locked" )



    
        
    

    

    

        

    