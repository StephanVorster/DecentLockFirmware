import sys
from Window import *
from MainSys import *


# timer = QTimer()
# timer.setSingleShot(True)

app = QtWidgets.QApplication(sys.argv)
mainUI = UI_MAIN()
mainUI.showFullScreen()
mainsys = MainSystem( mainUI )

# window.show()


# def t4done():
#     mainUI.LOCKING()
#     timer.timeout.disconnect()

# def t3done():
#     mainUI.UNLOCKED_SCREEN()
#     timer.timeout.disconnect()
#     timer.timeout.connect( t4done )
#     timer.start( 3000 )

# def t2done():
#     mainUI.ONLINE_MODE()
#     timer.stop()
#     timer.timeout.disconnect()
#     timer.timeout.connect( t3done )
#     timer.start( 3000 )

# def t1done():
#     mainUI.INITLOADING_LOCKEDSCREEN()
#     timer.timeout.disconnect()
#     timer.timeout.connect( t2done )
#     timer.start( 3000 )

# timer.timeout.connect( t1done )
# timer.start( 5000 )

sys.exit(app.exec())

# Steph@n135
# Before running on RPi launch
# run -> export DISPLAY=:0.0

"""
ssh -r ./* dev@10.0.0.101:~/AppLock/* 

"""




























































































































































































































































































    