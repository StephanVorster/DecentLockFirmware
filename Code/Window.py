from PySide6 import QtWidgets, QtGui
from UI_PKG import *
from JN_PKG import *
from UI_ICONS import *
from nfc_handler import nfcHandler
import time

class UI_MAIN(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bruh")
        self.setFixedSize(480, 800)
       
        # Load the PNG image
        # C:\\Users\\justi\\OneDrive - Sheridan College\\School\\CAPSTONE\\Lock-Software\\Python\\Resources\\GradientMainBG_AssetExport.png
        main_bg_pixmap = QtGui.QPixmap("/home/sv/Projects/rpi/DecentLockFirmware-UI/Resources/GradientMainBG_AssetExport.png")
        background_image = QtWidgets.QLabel(self)
        background_image.setPixmap(main_bg_pixmap)
        background_image.setGeometry(0, 0, self.width(), self.height())

        # Load icons
        self.jnIcon = UI_Icon()

        # Load Keypad
        self.keypad = UI_NumericKeypad( self.jnIcon, self )
        self.keypad.j_Entrance()

        # Create NFC Handler
        self.nfc = nfcHandler(self)



        

        





        
        