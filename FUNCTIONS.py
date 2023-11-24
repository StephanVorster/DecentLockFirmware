from PyQt5.QtCore import *



def FUNC_DISCONNECT_EVENTSIGNAL( sig:pyqtBoundSignal ) -> bool:

    """
    Disconnects pyqtBoundSignal object from QtCore\n
    Returns False if an error occured. 
    """
    try:
        sig.disconnect()
    except:
        return False
    
    return True


def FUNC_BETWEEN( source, value0, value1 ) -> bool:

    """
    Checks if `source` is between `value0` and `value1`\n
    Returns true if it is.
    Else false
    """

    if source >= value0 and source <= value1:
        return True
    else:
        return False
    
def FUNC_TRY_CALLING( func: object ) -> bool:

    """
    This is meant for calling a callback function through a variable that 
    might be a None type. 

    Returns True if successfully called the function
    """

    try:
        func()
    except:
        return False
    
    return True
    
