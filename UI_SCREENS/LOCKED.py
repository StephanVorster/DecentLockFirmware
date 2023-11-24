from JN_PKG import *
from UI_ICONS import *
from UI_SCREENS.COLORS import *


class UI_LOCKED():

    """
    ??
    """

    def __init__( self, border: JN_SVG_Widget, icons : UI_Icon, parent = None ) -> None:

        """
        ??
        """

        self.icon = icons

        self.appearance = False

        # Callback
        self.EXTCB_OFFLINE = None
        self.EXTCB_NFC = None

        # Initiate Lock Symbol
        self.L_SYMBOL = JN_SVG_Widget(parent)                      # Initiate the JN_SVG_Widget object
        self.L_SYMBOL.j_iconSet(icons.lock_locked)                  # Set the icon
        self.L_SYMBOL.j_featureSet(
            glow_onPR=True,     # Glow Config
            glow_anim=True,
            glow_color=UI_Color.RED.value,
            glow_upValue=50,
            shadow_on=True,     # Shadow
            scale_onPR=True,    # Scale Config
            scale_anim=True,
            scale_upValue=self.L_SYMBOL.j_increasedSize( 25 )
        )     
        self.L_SYMBOL.j_enableHold( 2000 )     
        self.L_SYMBOL.j_enableClick()      
        self.L_SYMBOL.j_setHoldCallback( self.INTER_HOLD_HANDLER )  
        self.L_SYMBOL.j_setPressCallback( self.INTER_PRESS_HANDLER )
        self.L_SYMBOL.j_setReleaseCallback( self.INTER_RELEASE_HANDLER )

        # Initiate Lock Ring
        self.L_RING = JN_SVG_Widget(parent)                      # Initiate the JN_SVG_Widget object
        self.L_RING.j_iconSet(icons.ring_red)                  # Set the icon
        self.L_RING.j_featureSet(
            scale_onPR=True,
            scale_anim=True,
            scale_upValue=self.L_RING.j_increasedSize( 50 )
        )

        # Timer 500ms delay for hold
        self.delay_timer : QTimer = QTimer()
        self.delay_timer.setInterval( 500 )
        self.delay_timer.setSingleShot( True )
        self.delay_timer.timeout.connect( 
            lambda: self.L_RING.j_animateScale( 
                size_end=self.L_RING.j_increasedSize( 50 ),
                duration=2000
            ) 
        )

        # Intiate the Border   
        self.BORDER = border

        self.L_SYMBOL.j_bringFront()                 
        
    def ENTRANCE(self):
        self.appearance = True
        self.L_RING.j_iconSet( self.icon.ring_red )
        self.L_SYMBOL.j_Entrance( animate=True )
        self.L_RING.j_Entrance( animate=True )
        self.BORDER.j_Entrance( animate=True )

    def EXIT_NFC(self):
        self.appearance = False
        self.L_RING.j_animateScaleStop()
        self.L_RING.inter_showScale( scaleUp=False, animate=True )
        self.L_RING.j_iconSet( self.icon.ring_red )
        self.L_RING.j_setExitCallback( lambda: FUNC_TRY_CALLING( self.EXTCB_NFC ) )
        self.L_SYMBOL.j_setExitCallback( lambda: self.L_RING.j_Exit(True) )
        self.L_SYMBOL.j_Exit( True )

    def SET_NFC_CB(self, nfc_cb):
        if nfc_cb is None: # Clear out signal
            self.EXTCB_NFC = None
        else: # Attached callback to signal
            self.EXTCB_NFC = nfc_cb
    
    def SET_OFFLINE_CB(self, off_cb):
        if off_cb is None: # Clear out signal
            self.EXTCB_OFFLINE = None
        else: # Attached callback to signal
            self.EXTCB_OFFLINE = off_cb

    def INTER_HOLD_HANDLER(self):
        self.appearance = False
        self.L_RING.j_animateScaleStop()
        self.L_RING.inter_showScale( scaleUp=False, animate=True )
        self.L_RING.j_iconSet( self.icon.ring_yellow )
        self.L_RING.j_setExitCallback( lambda: FUNC_TRY_CALLING(self.EXTCB_OFFLINE) )
        self.L_SYMBOL.j_setExitCallback( lambda: self.L_RING.j_Exit(True) )
        self.L_SYMBOL.j_Exit( True )

    def INTER_PRESS_HANDLER(self):
        self.delay_timer.start()
       
    def INTER_RELEASE_HANDLER(self):
        self.delay_timer.stop()
        self.L_RING.j_animateScaleStop()
        self.L_RING.inter_showScale( scaleUp=False, animate=True )
      
        