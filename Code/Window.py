from PyQt5 import QtWidgets, QtGui
from JN_PKG import *
from UI_ICONS import *
from UI_SCREENS.KEYPAD import *
from UI_SCREENS.BIO import *
from UI_SCREENS.NFC import *
from UI_SCREENS.UNLOCKED import *
from UI_SCREENS.LOCKED import *
from UI_SCREENS.LOADING import *


class UI_MAIN(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bruh")
        self.setFixedSize(480, 800)
        self.setAttribute( Qt.WidgetAttribute.WA_AcceptTouchEvents, True )
        # self.setCursor( Qt.CursorShape.BlankCursor )

        # Load icons
        self.jnIcon = UI_Icon()
       
        # Load the PNG image
        main_bg_pixmap = QtGui.QPixmap( self.jnIcon.path_bg )
        background_image = QtWidgets.QLabel(self)
        background_image.setPixmap(main_bg_pixmap)
        background_image.setGeometry(0, 0, self.width(), self.height())

        # Intiate the Borders
        # Small
        self.BORDER_SMALL = JN_SVG_Widget( self )
        self.BORDER_SMALL.j_iconSet( self.jnIcon.border_small )
        self.BORDER_SMALL.j_featureSet( scale_onPR=True )
        # Large
        self.BORDER_LARGE = JN_SVG_Widget( self )
        self.BORDER_LARGE.j_iconSet( self.jnIcon.border_large )
        self.BORDER_LARGE.j_featureSet( scale_onPR=True )

        self.loading = UI_LOADING( parent=self )

        self.keypad = UI_NumericKeypad( self.jnIcon, self )
        # self.keypad.j_Entrance()

        self.bio = UI_BIO( self.BORDER_SMALL, self.jnIcon, self )
        # self.bio.j_Entrance()

        self.nfc = UI_NFC( self.BORDER_SMALL, self.jnIcon, self )

        self.locked = UI_LOCKED( self.BORDER_SMALL, self.jnIcon, self )
        # self.locked.ENTRANCE()
        self.locked.SET_OFFLINE_CB( self.nfc.ENTRANCE )
        self.locked.SET_NFC_CB( self.loading.ENTRANCE )

        self.unlocked = UI_UNLOCKED( self.BORDER_SMALL, self.jnIcon, self )


        

    def INIT_LOADING_SYSTEM(self):
        self.loading.SET_TEXT( "System Loading" )
        self.loading.ENTRANCE() 

    def IDLE_LOCKED_SCREEN(self):

        self.loading.SET_EXTCB_EXIT( self.locked.ENTRANCE )
        self.loading.EXIT()

    def ONLINE_MODE(self):
        self.loading.SET_TEXT( "NFC\nWaiting to Authenticate" )
        self.loading.SET_EXTCB_EXIT(None)
        self.locked.SET_NFC_CB( self.loading.ENTRANCE )
        self.locked.EXIT_NFC()

    def UNLOCKED_SCREEN(self):
        self.loading.SET_EXTCB_EXIT( self.unlocked.ENTRANCE )
        self.loading.EXIT()

    def LOCKING( self ):
        self.unlocked.SET_EXTCB_EXIT( self.locked.ENTRANCE )
        self.unlocked.EXIT()

    



    
    

        
        



        
        

        
