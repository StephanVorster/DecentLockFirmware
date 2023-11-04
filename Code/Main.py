import sys
from Window import *

if __name__ == '__main__':
    print("Hello")
    app = QtWidgets.QApplication(sys.argv)
    window = UI_MAIN()
    window.show()
    sys.exit(app.exec())

    