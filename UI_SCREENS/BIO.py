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

        # CALLBACK
        self.EXTCB_ENTRANCE = None
        self.EXTCB_EXIT = None

        # Initiate Fingerprint Symbol
        self.BIO_SYMBOL = JN_SVG_Widget(parent)                      # Initiate the JN_SVG_Widget object
        self.BIO_SYMBOL.j_iconSet(icons.fp_symbol)                  # Set the icon
        self.BIO_SYMBOL.j_featureSet(
            scale_onPR=True,
            scale_animDuration=True
        )                            

        # Initiate Fingerprint Ring
        self.BIO_RING = JN_SVG_Widget(parent)                      # Initiate the JN_SVG_Widget object
        self.BIO_RING.j_iconSet(icons.fp_ring)                  # Set the icon
        self.BIO_RING.j_featureSet(
            scale_onPR=True,
            scale_animDuration=True
        )

                       
        
    def ENTRANCE(self):
        self.BIO_SYMBOL.j_setEntryCallback( self.EXTCB_ENTRANCE )
        self.BIO_SYMBOL.j_Entrance( animate=True )
        self.BIO_RING.j_Entrance( animate=True )

    def EXIT(self):
        self.BIO_SYMBOL.j_setExitCallback( self.EXTCB_EXIT )
        self.BIO_SYMBOL.j_Exit( animate=True )
        self.BIO_RING.j_Exit( animate=True )

    def SET_ENTRANCE_CB( self, cb = None ):
        if cb is None:
            self.EXTCB_ENTRANCE = None
        else:
            self.EXTCB_ENTRANCE = cb

    def SET_EXIT_CB( self, cb = None ):
        if cb is None:
            self.EXTCB_EXIT = None
        else:
            self.EXTCB_EXIT = cb