# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import serial
import adafruit_fingerprint
from PyQt5.QtWidgets import *
import serial
import serial.tools.list_ports
from PyQt5.QtCore import *
from FUNCTIONS import *
import enum



# import board
# uart = busio.UART(board.TX, board.RX, baudrate=57600)

# If using with a computer such as Linux/RaspberryPi, Mac, Windows with USB/serial converter:
# uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi and hardware UART:


# If using with Linux/Raspberry Pi 3 with pi3-disable-bt
# uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)



##################################################

class FINGERPRINT(QThread):

    class ACTION(enum.Enum):
        STANDBY = 0,
        ENROLL = 1,
        FIND = 2,
        CLEAR = 3

    class STATE(enum.Enum):

        ENROLL_F1       = 0,
        ENROLL_F2       = 1,
        ENROLL_DONE     = 2,
        ENROLL_ERROR    = 3,
    
        FIND            = 4,
        MATCHED         = 5,
        FAILED          = 6


    signal_status:pyqtSignal = pyqtSignal( STATE )
        


    def __init__(self, debug = False):
        super().__init__()

        self.uart = serial.Serial("/dev/ttyAMA2", baudrate=57600, timeout=1)
        self.finger = adafruit_fingerprint.Adafruit_Fingerprint(self.uart)

        self.state = self.ACTION.STANDBY


    def get_fingerprint(self):
        """Get a finger print image, template it, and see if it matches!"""
        if self.debug: print("Waiting for image...")
        while self.finger.get_image() != adafruit_fingerprint.OK:
            pass
        if self.debug: print("Templating...")
        if self.finger.image_2_tz(1) != adafruit_fingerprint.OK:
            return False
        if self.debug: print("Searching...")
        if self.finger.finger_search() != adafruit_fingerprint.OK:
            return False
        return True


    # pylint: disable=too-many-branches
    def get_fingerprint_detail(self):
        """Get a finger print image, template it, and see if it matches!
        This time, print out each error instead of just returning on failure"""
        if self.debug: print("Getting image...", end="")
        i = self.finger.get_image()
        if i == adafruit_fingerprint.OK:
            if self.debug: print("Image taken")
        else:
            if i == adafruit_fingerprint.NOFINGER:
                if self.debug: print("No finger detected")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                if self.debug: print("Imaging error")
            else:
                if self.debug: print("Other error")
            return False

        if self.debug: print("Templating...", end="")
        i = self.finger.image_2_tz(1)
        if i == adafruit_fingerprint.OK:
            if self.debug: print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                if self.debug: print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                if self.debug: print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                if self.debug: print("Image invalid")
            else:
                if self.debug: print("Other error")
            return False

        if self.debug: print("Searching...", end="")
        i = self.finger.finger_fast_search()
        # pylint: disable=no-else-return
        # This block needs to be refactored when it can be tested.
        if i == adafruit_fingerprint.OK:
            if self.debug: print("Found fingerprint!")
            return True
        else:
            if i == adafruit_fingerprint.NOTFOUND:
                if self.debug: print("No match found")
            else:
                if self.debug: print("Other error")
            return False


    # pylint: disable=too-many-statements
    def enroll_finger(self, location):
        """Take a 2 finger images and template it, then store in 'location'"""
        for fingerimg in range(1, 3):
            if fingerimg == 1:
                if self.debug: print("Place finger on sensor...", end="")
                self.signal_status.emit( self.STATE.ENROLL_F1 )
            else:
                if self.debug: print("Place same finger again...", end="")
                self.signal_status.emit( self.STATE.ENROLL_F2 )

            while True:
                i = self.finger.get_image()
                if i == adafruit_fingerprint.OK:
                    if self.debug: print("Image taken")
                    break
                if i == adafruit_fingerprint.NOFINGER:
                    if self.debug: print(".", end="")
                elif i == adafruit_fingerprint.IMAGEFAIL:
                    if self.debug: print("Imaging error")
                    self.signal_status.emit( self.STATE.ENROLL_ERROR )
                    return False
                else:
                    if self.debug: print("Other error")
                    self.signal_status.emit( self.STATE.ENROLL_ERROR )
                    return False

            if self.debug: print("Templating...", end="")
            i = self.finger.image_2_tz(fingerimg)
            if i == adafruit_fingerprint.OK:
                if self.debug: print("Templated")
            else:
                
                if i == adafruit_fingerprint.IMAGEMESS:
                    if self.debug: print("Image too messy")
                elif i == adafruit_fingerprint.FEATUREFAIL:
                    if self.debug: print("Could not identify features")
                elif i == adafruit_fingerprint.INVALIDIMAGE:
                    if self.debug: print("Image invalid")
                else:
                    if self.debug: print("Other error")

                self.signal_status.emit( self.STATE.ENROLL_ERROR )
                return False

            if fingerimg == 1:
                if self.debug: print("Remove finger")
                time.sleep(1)
                while i != adafruit_fingerprint.NOFINGER:
                    i = self.finger.get_image()

        if self.debug: print("Creating model...", end="")
        i = self.finger.create_model()
        if i == adafruit_fingerprint.OK:
            if self.debug: print("Created")
        else:
            if i == adafruit_fingerprint.ENROLLMISMATCH:
                if self.debug: print("Prints did not match")
                self.signal_status.emit( self.STATE.ENROLL_ERROR )
            else:
                if self.debug: print("Other error")
                self.signal_status.emit( self.STATE.ENROLL_ERROR )
            return False

        if self.debug: print("Storing model #%d..." % location, end="")
        i = self.finger.store_model(location)
        if i == adafruit_fingerprint.OK:
            if self.debug: print("Stored")
        else:
            if i == adafruit_fingerprint.BADLOCATION:
                if self.debug: print("Bad storage location")
            elif i == adafruit_fingerprint.FLASHERR:
                if self.debug: print("Flash storage error")
            else:
                if self.debug: print("Other error")

            self.signal_status.emit( self.STATE.ENROLL_ERROR )
            return False

        self.signal_status.emit( self.STATE.ENROLL_DONE )
        return True


    def save_fingerprint_image(self, filename):
        """Scan fingerprint then save image to filename."""
        while self.finger.get_image():
            pass

        # let PIL take care of the image headers and file structure
        from PIL import Image  # pylint: disable=import-outside-toplevel

        img = Image.new("L", (256, 288), "white")
        pixeldata = img.load()
        mask = 0b00001111
        result = self.finger.get_fpdata(sensorbuffer="image")

        # this block "unpacks" the data received from the fingerprint
        #   module then copies the image data to the image placeholder "img"
        #   pixel by pixel.  please refer to section 4.2.1 of the manual for
        #   more details.  thanks to Bastian Raschke and Danylo Esterman.
        # pylint: disable=invalid-name
        x = 0
        # pylint: disable=invalid-name
        y = 0
        # pylint: disable=consider-using-enumerate
        for i in range(len(result)):
            pixeldata[x, y] = (int(result[i]) >> 4) * 17
            x += 1
            pixeldata[x, y] = (int(result[i]) & mask) * 17
            if x == 255:
                x = 0
                y += 1
            else:
                x += 1

        if not img.save(filename):
            return True
        return False


    ##################################################


    def get_num(self, max_number):
        """Use input() to get a valid number from 0 to the maximum size
        of the library. Retry till success!"""
        i = -1
        while (i > max_number - 1) or (i < 0):
            try:
                i = int(input("Enter ID # from 0-{}: ".format(max_number - 1)))
            except ValueError:
                pass
        return i
    

    def SET_ACTION( self, state:ACTION ):
        
        self.state = state

    def check(self) -> bool:

        if self.finger.read_templates() != adafruit_fingerprint.OK:
            if self.debug: print("Failed to read templates")
            return False

        if self.debug: print("Fingerprint templates: ", self.finger.templates)
        if self.finger.count_templates() != adafruit_fingerprint.OK:
            if self.debug: print("Failed to read templates")
            return False
        
        if self.debug:  print("Number of templates found: ", self.finger.template_count)
        if self.finger.read_sysparam() != adafruit_fingerprint.OK:
            if self.debug: print("Failed to get system parameters")
            return False
        
        return True
        

    def run(self):

        while True:
            
            # print("Size of template library: ", self.finger.library_size)
            # print("e) enroll print")
            # print("f) find print")
            # print("d) delete print")
            # print("s) save fingerprint image")
            # print("r) reset library")
            # print("q) quit")
            # print("----------------")

            if self.state == self.ACTION.ENROLL:
                if not self.check():
                    self.signal_status.emit( self.STATE.ENROLL_ERROR )
                self.enroll_finger(self.get_num(self.finger.library_size))
                self.state = self.STATE.STANDBY

            elif self.state == self.ACTION.FIND:
                self.check()
                if self.get_fingerprint():
                    print("Detected #", self.finger.finger_id, "with confidence", self.finger.confidence)
                else:
                    print("Finger not found")

            # if c == "d":
            #     if self.finger.delete_model(self.get_num(self.finger.library_size)) == adafruit_fingerprint.OK:
            #         print("Deleted!")
            #     else:
            #         print("Failed to delete")

            elif self.state == self.ACTION.CLEAR:
                self.check()
                if self.finger.empty_library() == adafruit_fingerprint.OK:
                    print("Library empty!")
                else:
                    print("Failed to empty library")

            # if c == "q":
            #     print("Exiting fingerprint example program")
            #     raise SystemExit

            else:
                pass
