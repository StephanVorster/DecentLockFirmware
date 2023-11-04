from PyQt5 import QtWidgets, QtGui
from JN_PKG import *
from UI_ICONS import *
from UI_PKG import *

class UI_MAIN(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bruh")
        self.setFixedSize(480, 800)
       
        # Load the PNG image
        main_bg_pixmap = QtGui.QPixmap("Resources/GradientMainBG_AssetExport.png")
        background_image = QtWidgets.QLabel(self)
        background_image.setPixmap(main_bg_pixmap)
        background_image.setGeometry(0, 0, self.width(), self.height())

        # Load icons
        self.jnIcon = UI_Icon()

        self.keypad = UI_NumericKeypad( self.jnIcon, self )

        def ent(): print("ENTERTED")
        def exit(): print("LEFT")
        def kp():
            print("KEYPRESS")
            print(self.keypad.j_lastKeypress)
        def correct():
            print("CORRECT")
            print(self.keypad.j_passwordIndex)
            print(self.keypad.j_getRemainingAttempt())
            print(self.keypad.j_getRemainingPassword())
        def wrong():
            print("WRONG")
            print(self.keypad.j_passwordIndex)
            print(self.keypad.j_getRemainingAttempt())
            print(self.keypad.j_getRemainingPassword())

        # Load Keypad
        
        
        self.keypad.j_setCallbacks(
            after_entrance=ent,
            after_exit=exit,
            keypress=kp,
            correct=correct,
            wrong=wrong
        )
        self.keypad.j_Entrance()


        
