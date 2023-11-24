from JN_PKG import *
from UI_ICONS import *
from UI_SCREENS.COLORS import *


class UI_BIO():

    """
    ??
    """

    def __init__( self, border: JN_SVG_Widget, icons : UI_Icon, parent = None ) -> None:

        """
        ??
        """

        self.icon = icons

        # 

        # Initiate Fingerprint Symbol
        self.BIO_SYMBOL = JN_SVG_Widget(parent)                      # Initiate the JN_SVG_Widget object
        self.BIO_SYMBOL.j_iconSet(icons.fp_symbol)                  # Set the icon
        self.BIO_SYMBOL.j_featureSet(
            scale_onPR=True
        )                            

        # Initiate Fingerprint Ring
        self.BIO_RING = JN_SVG_Widget(parent)                      # Initiate the JN_SVG_Widget object
        self.BIO_RING.j_iconSet(icons.fp_ring)                  # Set the icon
        self.BIO_RING.j_featureSet(
            scale_onPR=True
        )

        # Intiate the Border   
        self.BORDER = border                    
        
    def j_Entrance(self):
        
        self.BIO_SYMBOL.j_Entrance( animate=True )
        self.BIO_RING.j_Entrance( animate=True )
        self.BORDER.j_Entrance( animate=True )
        