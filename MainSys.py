import sys
from Window import *
from NanoSerial import NANO
from nfc_handler import *
from Fingerprint import FINGERPRINT

class MainSystem():

    timer:QTimer = QTimer()
    timer_popup:QTimer = QTimer()

    def __init__(self, UI:UI_MAIN):

        self.UI = UI
        self.START_UP()

        

    def HANDLER_NANO_RX(self):
        pass

    def START_UP(self):

        print( "System Start UP" )

        self.timer.setSingleShot(True)

        self.nano = NANO( '/dev/ttyUSB1', 9600 )
        self.nano.rx_signal.connect( self.HANDLER_NANO_RX )
        self.nano.start()
        print("StartUp - Serial")

        # self.fingerprint = FINGERPRINT()
        # self.fingerprint.start()

        # Replace this as this is blocking
        while self.nano.state is not NANO.NANOSTATE.CONNECTED:
            pass

        self.nano.DOOR( NANO.DOORSTATE.UNLOCKED )

        self.nfc = nfc_auth_handler(debug=False)
        print("StartUp - NFC")

        

        # ( Loading - Entry )
        self.UI.loading.SET_TEXT( "System Loading" )
        self.UI.loading.ENTRANCE() 
        self.timer.timeout.connect( self.STARTUP_IDLE )
        self.timer.start(2000)
        print("StartUp - Screen")

        


    
    def STARTUP_IDLE(self):

        # ( Loading - Exit ) ----> ( Locked - Entrance )
        self.UI.loading.SET_EXTCB_EXIT( self.UI.locked.ENTRANCE )
        self.UI.loading.EXIT()

        self.UI.locked.SET_OFFLINE_CB( self.UI.keypad.ENTRANCE )

        # NFC Setup for ONLINE
        self.nfc.setStateReady(True)
        print("Idle - NFC Ready")

        def handler_onboard( success:bool ):
            print(f"onboard = {success}")
            if success:     self.ONBOARDING_INIT()
            else:           
                self.UI.pup.SET_TEXT("Onboarding Failed")
                self.UI.pup.ENTRANCE( duration=5000 )
                self.UI.locked.ENTRANCE()

        def handler_success( state:bool ):
            print(state)
            if state: self.ONLINEMODE_SUCCESS() # ---> AUTH SUCCESS
            else: self.ONLINEMODE_FAILED()      # ---> AUTH FAILED

        def handler_detect( detect:bool ):
            print("Detect:",detect)
            if detect: self.ONLINEMODE_WAIT()   # ---> Loading Screen

        self.nfc.auth_signal.connect( handler_success )
        self.nfc.detect_signal.connect( handler_detect )
        self.nfc.onboard_signal.connect( handler_onboard )

        self.nfc.start()
        print("Idle - NFC Thread Started")
        print("Waiting for NFC or OFFLINE activation")


    def ONLINEMODE_WAIT(self):

        print("ONLINE - Waiting for Authentication")

        # ( Locked - Exit ) ----> ( Loading - Entrance )
        self.UI.locked.SET_NFC_CB( self.UI.loading.ENTRANCE )
        self.UI.locked.EXIT_NFC()
        

    def ONLINEMODE_SUCCESS(self):

        # Turn Off NFC
        self.nfc.setStateReady(False)

        # Make sure to exit locked screen
        self.UI.locked.SET_NFC_CB(None)
        self.UI.locked.EXIT_NFC()

        # ( Loading - Exit ) ---> ( Unlocked - Entrance )
        self.UI.loading.SET_EXTCB_EXIT( self.UI.unlocked.ENTRANCE() )
        self.UI.loading.EXIT()

        # Unlock the Door Latch
        self.nano.DOOR( NANO.DOORSTATE.UNLOCKED )

        print( "UNLOCK - Waiting to open door" )

        print( "UNLOCK - Door Opened - Waiting to Close" ) 

        print( "UNLOCK - Opened for too long - Sound an alarm" )

        print( "UNLOCK - Door Closed - Locking" )

        print( "UNLOCK - Idle Timer Exceeded - Locking" )


    def ONLINEMODE_FAILED(self):

        # Make sure to exit locked screen
        self.UI.locked.SET_NFC_CB(None)
        self.UI.locked.EXIT_NFC()

        # ( Loading - Exit ) ---> ( Unlocked - Entrance )
        self.UI.loading.SET_TEXT("Authentication Failed")
        self.UI.loading.EXIT()

    def ONBOARDING_INIT(self):

        # Turn Off NFC
        self.nfc.setStateReady(False)

        def handler_afterMessage():
            self.UI.loading.SET_EXTCB_EXIT(self.UI.keypad.ENTRANCE)
            self.UI.loading.EXIT()

        def handler_keypad():

            address = self.nfc.last_onboarded_address
            existing_account_dict = None
			# Read the current accounts file tto the existing_account_dict variable
            with open('verified_accounts.json', 'r') as json_file:
                existing_account_dict = json.loads(json_file.read())
                if existing_account_dict is not None:
                    onboarded_address = ""
                    print( "searching for a key" )
                    for key in existing_account_dict.keys():
                        if "pin" not in list(existing_account_dict[key].keys()):
                            existing_account_dict[key]["pin"] = self.UI.keypad.USER_INPUT
                            print(f"Adding pin to {key}")
                            break
            
            
            with open('verified_accounts.json', 'w') as json_file:
                json.dump(existing_account_dict, json_file)
                print("Done Writng to JSON")

            
            self.ONBOARDING_FINGERPRINT()
            



        # Make sure to exit locked screen
        self.UI.loading.SET_TEXT( "ONBOARDING" )
        self.UI.loading.SET_EXTCB_EXIT(None)

        self.UI.locked.SET_NFC_CB(self.UI.loading.ENTRANCE)
        self.UI.locked.SET_OFFLINE_CB(None)
        self.UI.locked.EXIT_NFC()
        FUNC_DISCONNECT_EVENTSIGNAL( self.timer.timeout )
        self.timer.timeout.connect( handler_afterMessage )

        self.UI.keypad.PSWD_MODE = False
        self.UI.keypad.j_setCallbacks( correct=handler_keypad )

        self.timer.start(3000)

    def ONBOARDING_FINGERPRINT(self):
        
        print("234234")

        def handler_afterEntry():
            self.fingerprint.SET_ACTION( self.fingerprint.ACTION.ENROLL )

        def handler_fingerprint( status:FINGERPRINT.ACTION ):
            print( status.name )


        self.UI.bio.SET_ENTRANCE_CB( handler_afterEntry )
        self.UI.bio.ENTRANCE()
        
    

    

    

        

    