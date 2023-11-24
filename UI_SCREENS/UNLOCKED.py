from JN_PKG import *
from UI_ICONS import *
from UI_SCREENS.COLORS import *


class UI_UNLOCKED():

    """
    ??
    """

    def __init__( self, border: JN_SVG_Widget, icons : UI_Icon, parent = None ) -> None:

        """
        ??
        """

        self.icon = icons

        self.appearance = False;
        self.animUp = True;

        # Callback
        self.EXTCB_ENTRANCE = None
        self.EXTCB_EXIT = None

        # 
        def animToggle():
            self.INTER_BREATH( self.animUp )
            self.animUp = not self.animUp

        self.animation : QTimer = QTimer()
        self.animation.setInterval( 3000 )
        self.animation.setSingleShot(False)
        self.animation.timeout.connect( animToggle )

        # Initiate Unlock Symbol
        self.UL_SYMBOL = JN_SVG_Widget(parent)                      # Initiate the JN_SVG_Widget object
        self.UL_SYMBOL.j_iconSet(icons.lock_unlocked)                  # Set the icon
        self.UL_SYMBOL.j_featureSet(
            glow_onPR=True,     # Glow Config
            glow_anim=True,
            glow_color=UI_Color.GREEN.value,
            glow_upValue=50,
            scale_onPR=True,    # Scale Config
            scale_anim=True,
            scale_upValue=self.UL_SYMBOL.j_increasedSize( 25 )
        )                            

        # Initiate Unlock Ring
        self.UL_RING = JN_SVG_Widget(parent)                      # Initiate the JN_SVG_Widget object
        self.UL_RING.j_iconSet(icons.ring_green)                  # Set the icon
        self.UL_RING.j_featureSet(
            glow_onPR=True,     # Glow Config
            glow_anim=True,
            glow_color=UI_Color.GREEN.value,
            glow_upValue=50,
            scale_onPR=True,    # Scale Config
            scale_anim=True,
            scale_upValue=self.UL_RING.j_increasedSize( 50 ),

        )

        # Intiate the Border   
        self.BORDER = border            

    def INTER_BREATH( self, up:bool ):
        
        if up and self.appearance:
            self.UL_SYMBOL.j_animateScale( 
                size_end=self.UL_SYMBOL.j_increasedSize( 25 ),
                duration=1000
            )
            self.UL_SYMBOL.j_animateGlow( 
                blur_end=50,
                duration=1000,
                color=UI_Color.GREEN.value
            )
            self.UL_RING.j_animateScale( 
                size_end=self.UL_RING.j_increasedSize( 25 ),
                duration=1000
            )
            self.UL_RING.j_animateGlow( 
                blur_end=50,
                duration=1000,
                color=UI_Color.GREEN.value
            )
        elif not up and self.appearance:
            self.UL_SYMBOL.j_animateScale( 
                size_end=self.UL_SYMBOL.j_increasedSize( 0 ),
                duration=1200
            )
            self.UL_SYMBOL.j_animateGlow( 
                blur_end=0,
                duration=1200,
                color=UI_Color.GREEN.value
            )
            self.UL_RING.j_animateScale( 
                size_end=self.UL_RING.j_increasedSize( 0 ),
                duration=1200
            )
            self.UL_RING.j_animateGlow( 
                blur_end=0,
                duration=1200,
                color=UI_Color.GREEN.value
            )

        
    def ENTRANCE(self):
        self.appearance = True

        def afterEntry():
            self.animation.start()
            FUNC_TRY_CALLING( self.EXTCB_ENTRANCE )

        self.UL_SYMBOL.j_setEntryCallback( afterEntry )
        self.UL_SYMBOL.j_Entrance( animate=True )
        self.UL_RING.j_Entrance( animate=True )

    def EXIT(self):
        self.appearance = False

        self.animation.stop()
        self.UL_SYMBOL.j_setExitCallback( lambda: FUNC_TRY_CALLING( self.EXTCB_EXIT ) )
        self.UL_SYMBOL.j_Exit( animate=True )
        self.UL_RING.j_Exit( animate=True )

    def SET_ENTRY_CB(self, cb = None):
        self.EXTCB_ENTRANCE = cb
        
    def SET_EXTCB_EXIT(self, cb = None):
        self.EXTCB_EXIT = cb





  
        