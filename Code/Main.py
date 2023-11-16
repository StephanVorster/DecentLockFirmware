import sys
from Window import *
import time
import asyncio

# timer1:QTimer = QTimer()
# timer1.setSingleShot( True ) 

timer = QTimer()
timer.setSingleShot(True)

app = QtWidgets.QApplication(sys.argv)
window = UI_MAIN()
# window.showFullScreen()
window.show()

# window.INIT_LOADING_SYSTEM()

# def t4done():
#     window.LOCKING()
#     timer.timeout.disconnect()

# def t3done():
#     window.UNLOCKED_SCREEN()
#     timer.timeout.disconnect()
#     timer.timeout.connect( t4done )
#     timer.start( 3000 )

# def t2done():
#     window.ONLINE_MODE()
#     timer.stop()
#     timer.timeout.disconnect()
#     timer.timeout.connect( t3done )
#     timer.start( 3000 )

# def t1done():
#     window.IDLE_LOCKED_SCREEN()
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




























































































































































































































































































    