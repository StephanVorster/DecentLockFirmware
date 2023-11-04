from JN_PKG import *
from UI_ICONS import *
from typing import List

class UI_Color(Enum):
        SHADOW  = "#292929"
        GREEN   = "#00A651"
        YELLOW  = "#FBB040"
        RED     = "#EE3968"
        BLUE    = "#03AAB2"
        WHITE   = "#FFFFFF"



class UI_NumericKeypad():

    def __init__( self, icons : UI_Icon, parent = None ) -> None:

        self.icon = icons

        # Status
        self.rule_inputAttemptLimit : int = 2           # Max attempt per password
        self.rule_inputSizeLimit    : int = 10          # Max number of pswd digit
        self.rule_inputSizeMin      : int = 3           # Min number of pswd digit

        self.internalEntryExit      : bool = False      # True if j_entrance or j_exit is being used internally. To trigger entrance or exit cb for ext usage

        # Enablers
        self.en_key_reset   : bool = False
        self.en_key_enter   : bool = False
        self.en_key_wrong   : bool = False
        self.en_key_correct : bool = False

        def initKeyObjects( key : JN_SVG_Widget ):
            key.j_featureSet(
                 
                shadow_on=False,

                glow_onPR=True,
                glow_anim=True,
                glow_animDuration=100,
                glow_color=UI_Color.WHITE.value,
                glow_upValue=30,
                
                scale_onPR=True,
                scale_anim=True,
                scale_upValue=QSize( 110, 110 ),
                scale_animDuration=100,

                entrance_duration=300,
                exit_duration=300
                
            )
            key.j_Exit()
        
        self.key_1 = JN_SVG_Widget(parent)
        self.key_1.j_iconSet(icons.keypad_one)
        initKeyObjects(self.key_1)
        self.key_1.j_callbackRelease( self.key_1_event )

        self.key_2 = JN_SVG_Widget(parent)
        self.key_2.j_iconSet(icons.keypad_two)
        initKeyObjects(self.key_2)
        self.key_2.j_callbackRelease( self.key_2_event )

        self.key_3 = JN_SVG_Widget(parent)
        self.key_3.j_iconSet(icons.keypad_three)
        initKeyObjects(self.key_3)
        self.key_3.j_callbackRelease( self.key_3_event )

        self.key_4 = JN_SVG_Widget(parent)
        self.key_4.j_iconSet(icons.keypad_four)
        initKeyObjects(self.key_4)
        self.key_4.j_callbackRelease( self.key_4_event )

        self.key_5 = JN_SVG_Widget(parent)
        self.key_5.j_iconSet(icons.keypad_five)
        initKeyObjects(self.key_5)
        self.key_5.j_callbackRelease( self.key_5_event )

        self.key_6 = JN_SVG_Widget(parent)
        self.key_6.j_iconSet(icons.keypad_six)
        initKeyObjects(self.key_6)
        self.key_6.j_callbackRelease( self.key_6_event )

        self.key_7 = JN_SVG_Widget(parent)
        self.key_7.j_iconSet(icons.keypad_seven)
        initKeyObjects(self.key_7)
        self.key_7.j_callbackRelease( self.key_7_event )

        self.key_8 = JN_SVG_Widget(parent)
        self.key_8.j_iconSet(icons.keypad_eight)
        initKeyObjects(self.key_8)
        self.key_8.j_callbackRelease( self.key_8_event )

        self.key_9 = JN_SVG_Widget(parent)
        self.key_9.j_iconSet(icons.keypad_nine)
        initKeyObjects(self.key_9)
        self.key_9.j_callbackRelease( self.key_9_event )

        self.key_0 = JN_SVG_Widget(parent)
        self.key_0.j_iconSet(icons.keypad_zero)
        initKeyObjects(self.key_0)
        self.key_0.j_callbackRelease( self.key_0_event )

        self.key_enter = JN_SVG_Widget(parent)
        self.key_enter.j_iconSet(icons.keypad_enter)
        initKeyObjects(self.key_enter)
        self.key_enter.j_featureSet(
            glow_color = UI_Color.BLUE.value
        )
        self.key_enter.j_callbackRelease( self.key_e_event )
        self.key_enter.j_Exit()

        self.key_reset = JN_SVG_Widget(parent)
        self.key_reset.j_iconSet(icons.keypad_reset)
        initKeyObjects(self.key_reset)
        self.key_reset.j_featureSet(
            glow_color = UI_Color.RED.value
        )
        self.key_reset.j_callbackRelease( self.key_r_event )
        self.key_reset.j_Exit()

        self.key_correct = JN_SVG_Widget(parent)
        self.key_correct.j_iconSet(icons.keypad_correct)
        self.key_correct.j_featureSet( 
            shadow_on = False,
            glow_onPR=True
        )
        self.key_correct.j_enableClick( False )
        self.key_correct.j_Exit()

        self.key_wrong = JN_SVG_Widget(parent)
        self.key_wrong.j_iconSet(icons.keypad_wrong)
        self.key_wrong.j_featureSet( 
            shadow_on = False,
            glow_onPR=True
        )
        self.key_wrong.j_enableClick( False )
        self.key_wrong.j_Exit()

        self.key_enter.j_bringFront()

        self.key_0.j_setEntryExitCallbacks( entry=self.Handler_AfterEntryAnim )
        self.key_5.j_setEntryExitCallbacks( exit=self.Handler_AfterMainExit )
        self.key_6.j_setEntryExitCallbacks( entry=self.Handler_AfterMainEntry )
        self.ENABLE_ALL_KEYPRESSES( enable=False )

        # Timer
        def tmr_done(): 
            self.key_correct.j_Exit(animate=True)
        self.tmr = QTimer(parent)
        self.tmr.setSingleShot(True)
        self.tmr.setInterval( 2000 )
        self.tmr.timeout.connect( tmr_done )

        # Variables
        self.j_COMBINATION : List[str] = [ "12345", "54321" ]
        self.j_INPUT : str = ""
        self.j_passwordIndex : int = 0
        self.j_lastKeypress : int = None
        self.j_attempt : int = 0

        # Messages
        self.font : QFont = QFont("Bahnscript")
        self.message = QLabel( parent )
        self.message.setGeometry( 72, 214, 341, 58 )
        self.message.setAlignment( Qt.AlignmentFlag.AlignCenter )
        self.message.hide()

        self.msg_tryAgain   : tuple[ str, int, str ] = ("Incorrect PIN. Try Again", 16, UI_Color.WHITE.value)
        self.msg_EnterPin   : tuple[ str, int, str ] = ("Enter your PIN", 16, UI_Color.WHITE.value)
        self.msg_maxPinSize : tuple[ str, int, str ] = ("Maximum Digit Reached, Try Again", 16, UI_Color.WHITE.value)
    
        if self.j_COMBINATION.__len__() > 1:
            self.j_showMsgMultiPswd( self.j_passwordIndex )
        if self.j_COMBINATION.__len__() == 1:
            self.j_showMsg( self.msg_EnterPin )

        # CALL BACKS
        # LastKeypress
        # RemainingPassword
        # RemainingAttempt
        self.correct_cb = None
        self.wrong_cb = None
        self.afterEntrance_cb = None
        self.afterExit_cb = None
        self.keypress_cb = None

    def key_1_event(self): self.__KEYPRESS__( 1 )  
    def key_2_event(self): self.__KEYPRESS__( 2 )
    def key_3_event(self): self.__KEYPRESS__( 3 )
    def key_4_event(self): self.__KEYPRESS__( 4 )
    def key_5_event(self): self.__KEYPRESS__( 5 )
    def key_6_event(self): self.__KEYPRESS__( 6 )
    def key_7_event(self): self.__KEYPRESS__( 7 )
    def key_8_event(self): self.__KEYPRESS__( 8 )
    def key_9_event(self): self.__KEYPRESS__( 9 )
    def key_0_event(self): self.__KEYPRESS__( 0 )
    def key_e_event(self): self.__KEYPRESS__( 11 )
    def key_r_event(self): self.__KEYPRESS__( 22 )
    

    def j_Entrance(self):
        print("----ENTRANCE")

        def cb(): print("dfdfdfgdfg")

        self.key_1.j_Entrance(animate=True)
        self.key_2.j_Entrance(animate=True)
        self.key_3.j_Entrance(animate=True)
        self.key_4.j_Entrance(animate=True)
        self.key_5.j_Entrance(animate=True)
        self.key_6.j_Entrance(animate=True)
        self.key_7.j_Entrance(animate=True)
        self.key_8.j_Entrance(animate=True)
        self.key_9.j_Entrance(animate=True)
        self.key_0.j_Entrance(animate=True)


    def j_Exit(self):
        print("----EXIT")

        self.key_1.j_Exit(animate=True)
        self.key_2.j_Exit(animate=True)
        self.key_3.j_Exit(animate=True)
        self.key_4.j_Exit(animate=True)
        self.key_5.j_Exit(animate=True)
        self.key_6.j_Exit(animate=True)
        self.key_7.j_Exit(animate=True)
        self.key_8.j_Exit(animate=True)
        self.key_9.j_Exit(animate=True)
        self.key_0.j_Exit(animate=True)
        self.key_enter.j_Exit(animate=True)
        self.key_reset.j_Exit(animate=True)
        self.key_wrong.j_Exit(animate=True)
        self.ENABLE_ALL_KEYPRESSES( enable=False )

        
    
    def j_getRemainingPassword(self):
        return self.j_COMBINATION.__len__() - self.j_passwordIndex
    
    def j_getRemainingAttempt(self):
        return self.rule_inputAttemptLimit - self.j_attempt
    
    def j_setPassword(
        self,
        add:str = None,
        remove:str = None
    ):
        if add == "clear" or remove == "clear":
            self.j_COMBINATION.clear()
            return

        if add:
            self.j_COMBINATION.append( add )
            return

        if remove:
            self.j_COMBINATION.remove( remove )
            if self.j_COMBINATION.__len__() == 0:
                print("Empty")
            return
    
    def j_setRules(
        self,
        inputAttemptLimit = None,           
        inputSizeLimit = None,        
        inputSizeMin = None    
    ):
        if not inputAttemptLimit == "default":  self.rule_inputAttemptLimit = inputAttemptLimit        
        elif inputAttemptLimit == "default":    self.rule_inputAttemptLimit = 2
        
        if not inputSizeLimit == "default":     self.rule_inputSizeLimit    = inputSizeLimit         
        elif inputAttemptLimit == "default":    self.rule_inputSizeLimit    = 10
        
        if not inputSizeMin == "default":       self.rule_inputSizeMin      = inputSizeMin 
        elif inputAttemptLimit == "default":    self.rule_inputSizeMin      = 3

    def j_setCallbacks(
        self,
        after_entrance = None,
        after_exit = None,
        correct = None,
        wrong = None,
        keypress = None
    ):
        
        if not after_entrance == "clear":   self.afterEntrance_cb = after_entrance
        if after_entrance == "clear":       self.afterEntrance_cb = None

        if not after_exit == "clear":       self.afterExit_cb = after_exit
        if after_exit == "clear":           self.afterExit_cb = None
            
        if not correct == "clear":          self.correct_cb = correct
        if correct == "clear":              self.correct_cb = None

        if not wrong == "clear":            self.wrong_cb = wrong
        if wrong == "clear":                self.wrong_cb = None

        if not keypress == "clear":         self.keypress_cb = keypress
        if keypress == "clear":             self.keypress_cb = None

        
       


    def j_showMsg( self, msg:tuple[ str, int, str ] = None, show : bool = True, showAttempts:bool = False ):
        if show:
            
            message = msg[0]

            if showAttempts:
                message = self.SHOW_ATTEMPTS( msg[0] )

            self.message.setText( message )
            self.font.setPixelSize( msg[1] )
            self.message.setStyleSheet( f"color: {msg[2]}" )
            self.message.setFont( self.font )
            self.message.show()

        else:
            self.message.hide()
    
    def j_showMsgMultiPswd(self, index):

        number = index + 1
        message = f"Enter your your PIN {number}"

        msg = (
            message,
            self.msg_EnterPin[1],
            self.msg_EnterPin[2],
        )

        self.j_showMsg( msg )

    def ENABLE_ALL_KEYPRESSES( self, enable = True ):
        self.key_0.j_enableClick( enable )
        self.key_1.j_enableClick( enable )
        self.key_2.j_enableClick( enable )
        self.key_3.j_enableClick( enable )
        self.key_4.j_enableClick( enable )
        self.key_5.j_enableClick( enable )
        self.key_6.j_enableClick( enable )
        self.key_7.j_enableClick( enable )
        self.key_8.j_enableClick( enable )
        self.key_9.j_enableClick( enable )

    def Handler_AfterEntryAnim( self ):
        self.ENABLE_ALL_KEYPRESSES()

    def Handler_AfterMainEntry( self ):
        if not self.internalEntryExit:
            self.afterEntrance_cb()
        

    def Handler_AfterMainExit( self ):
        if not self.internalEntryExit:
            self.afterExit_cb()
    

    def SHOW_ATTEMPTS( self, msg:str ):

        number = self.rule_inputAttemptLimit - self.j_attempt

        if number == 1:
            msg += f"\n{number} more attempt"
        else:
            msg += f"\n{number} more attempts"

        return msg
    
    def __RESET_PSWD_INDEX__(self):
        self.j_passwordIndex = 0
    
    def __FULL_RESET__( self ):
        self.__RESET_INPUT__()
        # Reset Icons
        self.j_attempt = 0
        
    def __RESET_INPUT__( self ):
        self.j_INPUT = ""

        # Reset Buttons
        self.key_reset.j_Exit(animate=True) # Enter Button
        self.key_reset.j_enableClick( enable=False )
        self.en_key_reset = False
        
        self.key_enter.j_Exit(animate=True) # Reset Button
        self.key_enter.j_enableClick( enable=False )
        self.en_key_enter = False

        # Reset Icons
        self.en_key_correct = False
        self.en_key_correct = False


    def CHECK_ERRORS( self ):

        # Maximum Length Reached
        if self.j_INPUT.__len__() >= self.rule_inputSizeLimit:
            self.j_attempt += 1
            self.j_showMsg( self.msg_maxPinSize, showAttempts=True )
            self.__RESET_INPUT__()
        
        # Maximum Attempt Reached
        if self.j_attempt == self.rule_inputAttemptLimit:
            self.key_1.j_setEntryExitCallbacks( clear=True ) # Clear Callbacks with exiting set by next password
            self.internalEntryExit = True
            self.j_Exit()
            self.__FULL_RESET__()
            self.j_showMsg(show=False)
            print("Full Reset")

        return True
        
    def __KEYPRESS__(self, key:int = None):

        self.j_lastKeypress = key
        self.keypress_cb()

        # Add to user input
        if not key == 11 and not key == 22:

            self.j_INPUT += str(key)
            self.inputSize = self.j_INPUT.__len__()

            # Show the reset button after first digit
            if not self.en_key_reset and self.j_INPUT.__len__() == 1:

                def afterEntry(): 
                    self.key_reset.j_enableClick(enable=True)

                self.key_reset.j_Entrance(animate=True)
                self.key_reset.j_setEntryExitCallbacks( entry=afterEntry )
                self.en_key_reset = True

            # Show the enter button after minimum number of characters
            if not self.en_key_enter and self.j_INPUT.__len__() > self.rule_inputSizeMin:
                
                def afterEntry(): 
                    self.key_enter.j_enableClick(enable=True)

                if self.en_key_correct:

                    def correctExitDone(): 
                        self.key_correct.j_setEntryExitCallbacks( clear=True )
                        self.key_enter.j_setEntryExitCallbacks(entry=afterEntry)
                        self.key_enter.j_Entrance(animate=True)
                        self.en_key_enter = True

                    self.key_correct.j_setEntryExitCallbacks( exit=correctExitDone )
                    self.key_correct.j_Exit(animate=True)
                    self.en_key_correct = False

                else:

                    self.key_enter.j_Entrance(animate=True)
                    self.key_enter.j_setEntryExitCallbacks(entry=afterEntry)
                    self.en_key_enter = True
                
                
        else:

            if key == 11 and self.en_key_enter: # ENTER BUTTON

                if self.j_INPUT == self.j_COMBINATION[self.j_passwordIndex]: # Correct

                    self.correct_cb()
                    
                    def enterExitDone(): 
                        self.key_enter.j_setEntryExitCallbacks(clear=True)
                        self.key_correct.j_Entrance(True)
                        self.en_key_correct = True

                    def correctEntryDone(): 
                        self.key_correct.j_setEntryExitCallbacks(clear=True)
                        self.internalEntryExit = True
                        self.j_Exit()

                    self.j_passwordIndex += 1

                    if self.j_passwordIndex >= self.j_COMBINATION.__len__():  # All password are done
                        self.key_1.j_setEntryExitCallbacks( clear=True ) # Clear Callbacks with exiting set by next password
                        self.tmr.start()
                        self.internalEntryExit = False # Trigger external cb for exit
                        self.j_Exit()
                        self.__RESET_PSWD_INDEX__()

                    else:   # Next password
                        
                        def m():
                            self.j_showMsgMultiPswd( self.j_passwordIndex )
                            self.internalEntryExit = True
                            self.j_Entrance()

                        self.key_1.j_setEntryExitCallbacks( exit=m )
                        self.key_correct.j_setEntryExitCallbacks( entry = correctEntryDone )
                        
                    self.key_enter.j_setEntryExitCallbacks( exit = enterExitDone )
                    self.key_enter.j_Exit( animate=True )
                    self.key_enter.j_enableClick( enable=False )

                    self.en_key_enter = False
                    self.j_showMsg( show=False )

                    self.__FULL_RESET__()

                else:

                    self.j_attempt += 1
                    self.j_showMsg( self.msg_maxPinSize, showAttempts=True )
                    self.__RESET_INPUT__()

                    self.wrong_cb()

            if key == 22: # RESET BUTTON
                self.__RESET_INPUT__()
                   

        print( self.j_INPUT.__len__(), self.j_attempt, self.j_INPUT )

        self.CHECK_ERRORS()








    