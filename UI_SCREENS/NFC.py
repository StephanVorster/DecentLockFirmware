from JN_PKG import *
from UI_ICONS import *
from UI_SCREENS.COLORS import *


class UI_NFC():

    """
    ??
    """

    def __init__( self, border: JN_SVG_Widget, icons : UI_Icon, parent = None ) -> None:

        """
        ??
        """

        self.icon = icons

        # Callbacks
        self.EXTCB_EXIT = None

        # Initiate NFC Symbol
        self.NFC_SYMBOL = JN_SVG_Widget(parent)                      # Initiate the JN_SVG_Widget object
        self.NFC_SYMBOL.j_iconSet(icons.nfc_symbol)                  # Set the icon
        self.NFC_SYMBOL.j_featureSet(
            scale_onPR=True,
            scale_anim=True
        )                            

        # Initiate NFC Ring
        self.NFC_RING = JN_SVG_Widget(parent)                      # Initiate the JN_SVG_Widget object
        self.NFC_RING.j_iconSet(icons.nfc_ring)                  # Set the icon
        self.NFC_RING.j_featureSet(
            scale_onPR=True,
            scale_anim=True
        )

        # Intiate the Border   
        self.BORDER = border                    
        
    def ENTRANCE(self):
        
        self.NFC_SYMBOL.j_Entrance( animate=True )
        self.NFC_RING.j_Entrance( animate=True )
        self.BORDER.j_Entrance( animate=True )
        
    def EXIT(self):
        self.NFC_SYMBOL.j_Exit( animate=True )
        self.NFC_RING.j_Exit( animate=True )



    
