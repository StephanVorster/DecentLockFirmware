import sys
from Window import *

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet('Fusion')
    window = UI_MAIN()
    window.show()
    sys.exit(app.exec())

# import sys
# from PyQt5.QtWidgets import QApplication, QPushButton, QWidget

# def main():
#     app = QApplication(sys.argv)
#     window = QWidget()
#     window.setFixedSize( 300, 300 )
#     main_bg_pixmap = QtGui.QPixmap("Resources/GradientMainBG_AssetExport.png")
#     background_image = QtWidgets.QLabel(window)
#     background_image.setPixmap(main_bg_pixmap)
#     background_image.setGeometry(0, 0, window.width(), window.height())


    
#     button = QPushButton("Transparent Button")
#     button.setGeometry( 0,0,100,100 )
#     button.setFlat(True)
#     button.setStyleSheet("background: transparent;")
#     layout = QVBoxLayout()
#     layout.addWidget(button)
#     window.setLayout(layout)
#     window.show()
#     sys.exit(app.exec_())

#     def cb():
#         print("click")
#         button.setStyleSheet("background: transparent; border:None")
#     def cb2():
#         print("click")
#         button.setStyleSheet("background: transparent;")

#     button.pressed.connect(cb)
#     button.released.connect(cb2)



# if __name__ == "__main__":
#     main()






























































































































































































































































































    