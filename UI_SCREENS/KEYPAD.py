from JN_PKG import *
from UI_ICONS import *
from UI_SCREENS.COLORS import *
from typing import List

class UI_NumericKeypad():

    """
    This class utilizes the JN_SVG_WIDGET class to construct the Keypad
    """

    def __init__( self, icons : UI_Icon, parent = None ) -> None:

        """
        This class utilizes the JN_SVG_WIDGET class to construct the Keypad
        """

        self.icon = icons

        # Animation
        self.pref_entryexit_duration: int = 500
        self.pref_scale_duration    : int = 100

        # Status
        self.rule_inputAttemptLimit : int = 2           # Max attempt per password
        self.rule_inputSizeLimit    : int = 10          # Max number of pswd digit
        self.rule_inputSizeMin      : int = 3           # Min number of pswd digit

        # Enablers
        self.en_appearance      : bool = False
        self.en_key_reset       : bool = False
        self.en_key_enter       : bool = False
        self.en_icon_wrong      : bool = False
        self.en_icon_correct    : bool = False
        self.en_debug           : bool = True
 
        # Initiate all keys with this configuratiun
        def initKeyObjects( key : JN_SVG_Widget ):
            key.j_featureSet(
                 
                glow_onPR=True,
                glow_anim=True,
                glow_animDuration=200,
                glow_color=UI_Color.WHITE.value,
                glow_upValue=30,
                
                shadow_on=False,

                scale_onPR=True,
                scale_anim=True,
                scale_upValue=QSize( 110, 110 ),
                scale_animDuration=self.pref_scale_duration
                
            )
            key.j_enableClick()
        

        # NUMERIC KEYS

        # Initiates Key Number -- 1
        self.key_1 = JN_SVG_Widget(parent)                      # Initiate the JN_SVG_Widget object
        self.key_1.j_iconSet(icons.keypad_one)                  # Set the icon
        initKeyObjects(self.key_1)                              # Set JN_SVG_Widget object configuation
        self.key_1.j_setReleaseCallback( self.key_1_event )     # Set Callbacks
                                                                # This configuration is same to all numeric keys

        # Initiates Key Number -- 2
        self.key_2 = JN_SVG_Widget(parent)
        self.key_2.j_iconSet(icons.keypad_two)
        initKeyObjects(self.key_2)
        self.key_2.j_setReleaseCallback( self.key_2_event )

        # Initiates Key Number -- 3
        self.key_3 = JN_SVG_Widget(parent)
        self.key_3.j_iconSet(icons.keypad_three)
        initKeyObjects(self.key_3)
        self.key_3.j_setReleaseCallback( self.key_3_event )

        # Initiates Key Number -- 4
        self.key_4 = JN_SVG_Widget(parent)
        self.key_4.j_iconSet(icons.keypad_four)
        initKeyObjects(self.key_4)
        self.key_4.j_setReleaseCallback( self.key_4_event )

        # Initiates Key Number -- 5
        self.key_5 = JN_SVG_Widget(parent)
        self.key_5.j_iconSet(icons.keypad_five)
        initKeyObjects(self.key_5)
        self.key_5.j_setReleaseCallback( self.key_5_event )

        # Initiates Key Number -- 6
        self.key_6 = JN_SVG_Widget(parent)
        self.key_6.j_iconSet(icons.keypad_six)
        initKeyObjects(self.key_6)
        self.key_6.j_setReleaseCallback( self.key_6_event )

        # Initiates Key Number -- 7
        self.key_7 = JN_SVG_Widget(parent)
        self.key_7.j_iconSet(icons.keypad_seven)
        initKeyObjects(self.key_7)
        self.key_7.j_setReleaseCallback( self.key_7_event )

        # Initiates Key Number -- 8
        self.key_8 = JN_SVG_Widget(parent)
        self.key_8.j_iconSet(icons.keypad_eight)
        initKeyObjects(self.key_8)
        self.key_8.j_setReleaseCallback( self.key_8_event )

        # Initiates Key Number -- 9
        self.key_9 = JN_SVG_Widget(parent)
        self.key_9.j_iconSet(icons.keypad_nine)
        initKeyObjects(self.key_9)
        self.key_9.j_setReleaseCallback( self.key_9_event )

        # Initiates Key Number -- 0
        self.key_0 = JN_SVG_Widget(parent)
        self.key_0.j_iconSet(icons.keypad_zero)
        initKeyObjects(self.key_0)
        self.key_0.j_setReleaseCallback( self.key_0_event )

        # FUNCTION KEYS

        # Initiates ENTER Key
        self.key_enter = JN_SVG_Widget(parent)
        self.key_enter.j_iconSet(icons.keypad_enter)
        initKeyObjects(self.key_enter)
        self.key_enter.j_featureSet(                
            glow_color = UI_Color.BLUE.value                        # Set Glow Color
        )
        self.key_enter.j_setReleaseCallback( self.key_e_event )     # Set Callback
        self.key_enter.j_enableClick()                         # Initiately not clickable
        self.key_enter.j_bringFront()                               

        # Initiates RESET Key
        self.key_reset = JN_SVG_Widget(parent)
        self.key_reset.j_iconSet(icons.keypad_reset)
        initKeyObjects(self.key_reset)
        self.key_reset.j_featureSet(
            glow_color = UI_Color.RED.value                     
        )
        self.key_reset.j_setReleaseCallback( self.key_r_event )     
        self.key_reset.j_enableClick()

        # STATUS ICONS

        # Initiates CORRECT Status Icon 
        self.icon_correct = JN_SVG_Widget(parent)
        self.icon_correct.j_iconSet(icons.keypad_correct)
        self.icon_correct.j_featureSet( 
            shadow_on = False,
            glow_onPR=True
        )
        self.icon_correct.j_enableClick( False )

        # Initiates WRONG Status Icon 
        self.icon_wrong = JN_SVG_Widget(parent)
        self.icon_wrong.j_iconSet(icons.keypad_wrong)
        self.icon_wrong.j_featureSet( 
            shadow_on = False,
            glow_onPR=True
        )
        self.icon_wrong.j_enableClick( False )

         
        # CLASS MAIN CALLBACKS
    

        # TIMER - For delayed display of CORRECT Status Icon
        def tmr_done(): 
            self.icon_correct.j_Exit(animate=True)
        self.tmr = QTimer(parent)
        self.tmr.setSingleShot(True)
        self.tmr.setInterval( 2000 )
        self.tmr.timeout.connect( tmr_done )

        # VARIABLES
        # These variables can be access publicly
        self.j_COMBINATION : List[str] = [ "12345" ]
        """Password Source"""   
        self.USER_INPUT : str = ""     
        """Password User Input"""                            
        self.PSWD_INDEX : int = 0    
        """To select within the password COMBINATION array"""                     
        self.LAST_KEY : int = None 
        """Holds the most recent key that was pressed"""                       
        self.ATTEMPT_COUNT : int = 0         
        """Number of attempt after incorrect password"""       

        self.PSWD_MODE : bool = True # True means it is password mode            

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
            self.j_showMsgMultiPswd( self.PSWD_INDEX, False )
        if self.j_COMBINATION.__len__() == 1:
            self.j_showMsg( self.msg_EnterPin, False )

        # CALL BACKS
        self.EXTCB_CORRECT      = None
        self.EXTCB_WRONG        = None
        self.EXTCB_ENTRANCE     = None
        self.EXTCB_EXIT         = None
        self.EXTCB_KEYPRESS     = None

    def key_1_event(self): self.HANDLER_KEYPRESS( 1 )
    def key_2_event(self): self.HANDLER_KEYPRESS( 2 )
    def key_3_event(self): self.HANDLER_KEYPRESS( 3 )
    def key_4_event(self): self.HANDLER_KEYPRESS( 4 )
    def key_5_event(self): self.HANDLER_KEYPRESS( 5 )
    def key_6_event(self): self.HANDLER_KEYPRESS( 6 )
    def key_7_event(self): self.HANDLER_KEYPRESS( 7 )
    def key_8_event(self): self.HANDLER_KEYPRESS( 8 )
    def key_9_event(self): self.HANDLER_KEYPRESS( 9 )
    def key_0_event(self): self.HANDLER_KEYPRESS( 0 )
    def key_e_event(self): self.HANDLER_KEYPRESS( 11 )
    def key_r_event(self): self.HANDLER_KEYPRESS( 22 )

    def INTER_NUMKEYS( self, show = True, callback = None ):
        """
        Show/Remove number keys with animation
        """
        if show:
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
            self.key_0.j_setEntryCallback( callback )
        else:
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
            self.key_0.j_setExitCallback( callback )

    def INTER_DISPLAY_FUNCKEYS( 
        self, 
        show: bool = True, 
        key: JN_SVG_Widget = None
    ):
        
        # Callback
        def callback():
            # Clear Callback
            key.j_setExitCallback()  
            key.j_setEntryCallback()
            # Revert scale duration
            key.j_featureSet( scale_animDuration=self.pref_scale_duration )
        
        key.j_featureSet( scale_animDuration=self.pref_entryexit_duration )
        
        
        if show:
            key.j_setEntryCallback( callback ) # Assign a callback
            key.j_Entrance( animate=True )
        else:
            key.j_setExitCallback( callback ) # Assign a callback
            key.j_Exit( animate=True )

    def INTER_ENTER_KEY( self, show = True ):
        """
        Will show ENTER key depends on some states.\n
        Doesn't rely on `en_key_enter` status variable
        ### If already shown and `show=False`\n
        - Enter Key will be remove\n 
        ### If already shown and `show=True`\n
        - Remove if `USER_INPUT is empty`
        ### If not shown and `show=True`.\n
        - Show if USER INPUT reached the `rule_inputSizeMin` or more\n

        ### However\n
        - If the whole keypad is set to be not visible, this key will be remove ignoring `show=True`
        """

        # Initial Checks
        # if whole Keypad is not visible
        if not self.en_appearance:
            if self.key_enter.en_appearance: # Enter Key Visible -> Remove
                self.INTER_DISPLAY_FUNCKEYS( show=False, key=self.key_enter )
                self.en_key_enter = False
            return # Reset Key already not visible

        # Already shown
        if self.key_enter.en_appearance:
            if not show: # Remove
                self.INTER_DISPLAY_FUNCKEYS( show=False, key=self.key_enter )
                self.en_key_enter = False
            else: # If show
                # If USER INPUT is empty -> Remove this
                if self.USER_INPUT.__len__() == 0:
                    self.INTER_DISPLAY_FUNCKEYS( show=False, key=self.key_enter )
                    self.en_key_enter = False
                
        # Not shown
        else:
            if show:
                # If USER INPUT contains min # of input size defined or more, show
                if self.USER_INPUT.__len__() >= self.rule_inputSizeMin:
                    self.INTER_DISPLAY_FUNCKEYS( show=True, key=self.key_enter )
                    self.en_key_enter = True
            else:
                # Do nothing
                return
        
        return


    def INTER_RESET_KEY( self, show = True ):
        """
        Will show RESET key depends on some states.\n
        Doesn't rely on `en_key_reset` status variable
        ### If already shown and `show=False`\n
        - Reset Key will be remove\n 
        ### If already shown and `show=True`\n
        - Remove if `USER_INPUT is empty`
        ### If not shown and `show=True`.\n
        - Show if there are 1 or more character in `USER_INPUT`\n

        ### However\n
        - If the whole keypad is set to be not visible, this key will be remove ignoring `show=True`
        """

        # Initial Checks
        # if whole Keypad is not visible
        if not self.en_appearance:
            if self.key_reset.en_appearance: # Reset Key Visible -> Remove
                self.INTER_DISPLAY_FUNCKEYS( show=False, key=self.key_reset )  # REMOVE
                self.en_key_reset = False
                
            return # Reset Key already not visible

        # Already shown
        if self.key_reset.en_appearance:
            if not show: # Remove
                self.INTER_DISPLAY_FUNCKEYS( show=False, key=self.key_reset ) # REMOVE
                self.en_key_reset = False
                return
            else: # If show
                # If USER INPUT is empty -> Remove this
                if self.USER_INPUT.__len__() == 0:
                    self.INTER_DISPLAY_FUNCKEYS( show=False, key=self.key_reset )
                    self.en_key_reset = False
                
        # Not shown
        else:
            if show:
                
                # If INPUT contains 1 or more, show
                if self.USER_INPUT.__len__() >= 1:
                    self.INTER_DISPLAY_FUNCKEYS(  show=True, key=self.key_reset  ) # SHOW
                    self.en_key_reset = True
                    return
        
        
        return
    
    def INTER_CORRECT_ICON( self, show = True ):
        """
        Will show CORRECT Icon depends on some states.\n
        Doesn't rely on `en_icon_correct` status variable\n
        ### Function \n
        - `show=True` show the correct icon\n 
        - `show=False` remove the correct icon\n
        - There are no checking in this method. It is a simple show or hide function
        - `icon_correct` can be shown after keypad exit. In this state, the timer will remove this icon after some delay
        """

        # At this state, all password is correct and the whole keypad called exit
        # Intiate the timer
        if not self.en_appearance:

            def tmr_done(): # Exit Correct Icon
                self.icon_correct.j_Exit(animate=True)
                self.en_icon_correct = False

            self.tmr.setSingleShot(True)
            self.tmr.setInterval( 2000 ) # 2 seconds delay
            self.tmr.timeout.connect( tmr_done )

        # SHOW
        if show:
            # Icon not visible
            if not self.icon_correct.en_appearance:
                self.icon_correct.j_Entrance( animate=True )
                self.en_icon_correct = True 
                return
            # Icon already visible
            else:
                return
        # REMOVE
        else:
            # Icon visible
            if self.icon_correct.en_appearance:
                self.icon_correct.j_Exit( animate=True )
                self.en_icon_correct = False 
                return
            # Icon already not Visible
            else:
                return
            
    def INTER_WRONG_ICON( self, show = True ):
        """
        Will show WRONG Icon depends on some states.\n
        Doesn't rely on `en_icon_wrong` status variable\n
        ### Function \n
        - `show=True` show the wrong icon\n 
        - `show=False` remove the wrong icon\n
        ### However\n
        - If the whole keypad is set to be not visible, this icon will be remove ignoring `show=True`
        """

        # Initial Checks
        # if whole Keypad is not visible
        if not self.en_appearance:
            if self.icon_wrong.en_appearance: # Icon Wrong Visible -> Remove
                self.icon_wrong.j_Exit( animate=True )
                self.en_icon_wrong = False
            return # Icon Key already not visible

        # SHOW
        if show:
            # Icon not visible
            if not self.icon_wrong.en_appearance:
                self.icon_wrong.j_Entrance( animate=True )
                self.en_icon_wrong = True 
                return
            # Icon already visible
            else:
                return
        # REMOVE
        else:
            # Icon visible
            if self.icon_wrong.en_appearance:
                self.icon_wrong.j_Exit( animate=True )
                self.en_icon_wrong = False 
                return
            # Icon already not Visible
            else:
                return
        
    



    def ENTRANCE(self):

        """
        Animated Entrance of Keypad Screen\n
        Number keys will only be shown on the entrance.\n
        Icons and other Keys such Enter Key or Reset Key will be shown by certain actions.\n
        
        ### Note:\n
        - Keys are not clickable during animation\n
        - Clickable after Entrance Animation\n
        """

        self.en_appearance = True

        if self.en_debug: print("----ENTRANCE")

        # Make sure all function keys and icons are not visible
        if self.key_enter.en_appearance:                # ENTER KEY
            self.key_enter.j_Exit( animate=False )
        if self.key_reset.en_appearance:                # RESET KEY
            self.key_reset.j_Exit( animate=False )
        if self.icon_correct.en_appearance:             # CORRECT ICON
            self.icon_correct.j_Exit( animate=False )
        if self.icon_wrong.en_appearance:               # WRONG ICON
            self.icon_wrong.j_Exit( animate=False )

        # Callback
        def callback():
            FUNC_TRY_CALLING( self.EXTCB_ENTRANCE )
            # Revert scale duration to prefered
            self.INTER_ANIMSCALE_DURATION( duration=self.pref_scale_duration )

        # Temporarly set scale duration for Entrance
        self.INTER_ANIMSCALE_DURATION( duration=self.pref_entryexit_duration )
        self.INTER_NUMKEYS( show=True, callback=callback )


    def j_Exit(self):

        """
        Animated Exit of the Keypad Screen\n
        Keys are not clickable during animation
        """
        
        self.en_appearance = False

        if self.en_debug: print("----EXIT")

        # Callback
        def callback():
            FUNC_TRY_CALLING( self.EXTCB_EXIT )
            # Revert scale duration to prefered
            self.INTER_ANIMSCALE_DURATION( duration=self.pref_scale_duration )

        # Temporarly set scale duration for Entrance
        self.INTER_ANIMSCALE_DURATION( duration=self.pref_entryexit_duration )

        # Remove all keys and icons except CORRECT ICON as this will be removed by a timer
        self.INTER_NUMKEYS( show=False, callback=callback )
        self.INTER_ENTER_KEY( show=False )
        self.INTER_RESET_KEY( show=False )
        self.INTER_WRONG_ICON( show=False )
        

        
    def j_getRemainingPassword(self):
        """Returns the number of remaining password to be entered in the password COMBINATION array"""
        return self.j_COMBINATION.__len__() - self.PSWD_INDEX
    
    def j_getRemainingAttempt(self):
        """Returns the remaining number of attempt after unsuccessful password entry"""
        return self.rule_inputAttemptLimit - self.ATTEMPT_COUNT
    
    def j_setPassword(
        self,
        value   :str = None,
        mode    :int = None
    ):
        """
        Modifies the password COMBINATION array\n
        
        ### Method\n
        - `0` = Add `value` to the list as the most recent
        - `1` = Remove `value` to the list
        - `2` = Remove the 1st password on the list
        - `3` = Remove the last or most recent password on the list
        - `4` = Clear the list
        ### Error Code Return
        - `0` - SUCCESSFUL
        - `1` - UNSUCESSFUL - REMOVE VALUE, CANNOT FIND `value`
        - `2` - UNSUCESSFUL - REMOVE 1st PASS
        - `3` - UNSUCESSFUL - REMOVE LAST PASS
        - `4` - UNSUCESSFUL - CLEAR
        """
        pass


    def j_setCallbacks(
        self,
        after_entrance = None,
        after_exit = None,
        correct = None,
        wrong = None,
        keypress = None
    ):
        
        """
        To assign callbacks when:\n
        - `after_entrance` callback after entrance animation
        - `after_exit` callback after exit animation
        - `correct` callback whenever a correct password attempt
        - `wrong` callback whenever a wrong password attempt
        - `keypress` callback whenever a keypress action occured\n
        `=clear` to any parameter will clear the callback to that event

        """
        
        if not after_entrance == "clear":   self.EXTCB_ENTRANCE = after_entrance
        if after_entrance == "clear":       self.EXTCB_ENTRANCE = None

        if not after_exit == "clear":       self.EXTCB_EXIT = after_exit
        if after_exit == "clear":           self.EXTCB_EXIT = None
            
        if not correct == "clear":          self.EXTCB_CORRECT = correct
        if correct == "clear":              self.EXTCB_CORRECT = None

        if not wrong == "clear":            self.EXTCB_WRONG = wrong
        if wrong == "clear":                self.EXTCB_WRONG = None

        if not keypress == "clear":         self.EXTCB_KEYPRESS = keypress
        if keypress == "clear":             self.EXTCB_KEYPRESS = None

        
       

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
    
    def j_showMsgMultiPswd(self, index, show : bool):

        number = index + 1
        message = f"Enter your your PIN {number}"

        msg = (
            message,
            self.msg_EnterPin[1],
            self.msg_EnterPin[2],
        )

        self.j_showMsg( msg, show )


    def INTER_ANIMSCALE_DURATION( self, duration: int = 500 ):
        """For all keys and icons. Adjusts the duration of the scale animation. Used when exit and entrance as these uses different duration from on press scaling animation"""
        self.key_0.j_featureSet(        scale_animDuration = duration )
        self.key_1.j_featureSet(        scale_animDuration = duration )
        self.key_2.j_featureSet(        scale_animDuration = duration )
        self.key_3.j_featureSet(        scale_animDuration = duration )
        self.key_4.j_featureSet(        scale_animDuration = duration )
        self.key_5.j_featureSet(        scale_animDuration = duration )
        self.key_6.j_featureSet(        scale_animDuration = duration )
        self.key_7.j_featureSet(        scale_animDuration = duration )
        self.key_8.j_featureSet(        scale_animDuration = duration )
        self.key_9.j_featureSet(        scale_animDuration = duration )
        self.key_enter.j_featureSet(    scale_animDuration = duration )
        self.key_reset.j_featureSet(    scale_animDuration = duration )
        self.icon_correct.j_featureSet( scale_animDuration = duration )
        self.icon_wrong.j_featureSet(   scale_animDuration = duration )


    def SHOW_ATTEMPTS( self, msg:str ):

        number = self.rule_inputAttemptLimit - self.ATTEMPT_COUNT

        if number == 1:
            msg += f"\n{number} more attempt"
        else:
            msg += f"\n{number} more attempts"

        return msg
    

    def INTER_CHECK_PASSWORD( self ) -> bool:
        """
        Internal Use Only. Compares the `USER_INPUT` and `COMBINATION[PSWD_INDEX]`
        ### CORRECT:\n
        - Returns TRUE
        - Show Correct Icon
        - Increment `PSWD_INDEX` for next password
        - If there are no more password left, exit the whole keypad
        - Reset `USER_INPUT`
        - Show Message
        ### WRONG:\n
        - Returns FALSE
        - Show Wrong Icon
        - Increment `ATTEMPT_COUNT`
        - Reset `USER_INPUT`
        - Show Message
        """

        if self.USER_INPUT == self.j_COMBINATION[self.PSWD_INDEX]:
            print("Correct")
            
            # Check if there are anymore password in the list
            if not self.j_getRemainingPassword() == 0: # MORE
                self.PSWD_INDEX += 1 
            else:   # NO MORE
                self.j_Exit()

            
            self.INTER_CORRECT_ICON( show=True )
            self.INTER_WRONG_ICON( show=False )
            self.USER_INPUT = ""

            return True
        else:
            print("Wrong")

            # Check if attempt count exceeded
            if not self.j_getRemainingAttempt() == 0: # MORE
                self.ATTEMPT_COUNT += 1 
            else:   # NO MORE
                self.j_Exit()

            self.INTER_CORRECT_ICON( show=False )
            self.INTER_WRONG_ICON( show=True )
            self.USER_INPUT = ""




    def HANDLER_KEYPRESS(self, key:int = None):

        self.LAST_KEY = key

        FUNC_TRY_CALLING( self.EXTCB_KEYPRESS )

        # Add the keypress to input
        if key <= 9: # Digits only. No Function Keys
            self.USER_INPUT += str(key)

        # Function Key - RESET
        if key == 22 and self.en_appearance and self.en_key_reset: 
            print("Reset")
            self.USER_INPUT = ""

        # Function Key - ENTER
        if key == 11 and self.en_appearance and self.en_key_enter: 
            print("Enter")

            if self.PSWD_MODE:
                # Check Password 
                self.INTER_CHECK_PASSWORD()
            else:
                print(self.EXTCB_CORRECT)
                self.EXTCB_CORRECT()
                self.j_Exit()

        # Show Reset Key. The Function will do the checking if appropriate to show
        self.INTER_RESET_KEY()

        # Show Enter Key. The Function will do the checking if appropriate to show
        self.INTER_ENTER_KEY()
        

        if self.en_debug: 
            print( self.USER_INPUT.__len__(), self.ATTEMPT_COUNT, self.USER_INPUT )
        
        

