# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import serial
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, QThread
import adafruit_fingerprint

class fingerprint(QWidget):

    # import board
    # uart = busio.UART(board.TX, board.RX, baudrate=57600)

    # If using with a computer such as Linux/RaspberryPi, Mac, Windows with USB/serial converter:
    # self.uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

    # If using with Linux/Raspberry Pi and hardware UART:
    # uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

    # If using with Linux/Raspberry Pi 3 with pi3-disable-bt
    # uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)

    # self.finger = adafruit_fingerprint.Adafruit_Fingerprint(self.uart)

    ##################################################

    finger_auth_signal = pyqtSignal(bool)
    finger_enrolled_signal = pyqtSignal(bool)
    def __init__(self, uart_interface, led_color, led_mode):
        # self.led_color = 1
        # self.led_mode = 3
        self.led_color = led_color
        self.led_mode = led_mode
        # "/dev/ttyUSB0"
        self.uart = serial.Serial(uart_interface, baudrate=57600, timeout=1)
        self.finger = adafruit_fingerprint.Adafruit_Fingerprint(self.uart)
        self.finger.set_led(color=self.led_color, mode=self.led_mode)


    def get_fingerprint(self):
        """Get a fingerprint image, template it, and see if it matches!"""
        print("Waiting for image...")
        while self.finger.get_image() != adafruit_fingerprint.OK:
            pass
        print("Templating...")
        if self.finger.image_2_tz(1) != adafruit_fingerprint.OK:
            return False
        print("Searching...")
        if self.finger.finger_search() != adafruit_fingerprint.OK:
            return False
        return True


    # pylint: disable=too-many-branches
    def get_fingerprint_detail(self):
        """Get a fingerprint image, template it, and see if it matches!
        This time, print out each error instead of just returning on failure"""
        print("Getting image...", end="")
        i = self.finger.get_image()
        if i == adafruit_fingerprint.OK:
            print("Image taken")
        else:
            if i == adafruit_fingerprint.NOFINGER:
                print("No finger detected")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
            else:
                print("Other error")
            return False

        print("Templating...", end="")
        i = self.finger.image_2_tz(1)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

        print("Searching...", end="")
        i = self.finger.finger_fast_search()
        # pylint: disable=no-else-return
        # This block needs to be refactored when it can be tested.
        if i == adafruit_fingerprint.OK:
            print("Found fingerprint!")
            return True
        else:
            if i == adafruit_fingerprint.NOTFOUND:
                print("No match found")
            else:
                print("Other error")
            return False


    # pylint: disable=too-many-statements
    def enroll_finger(self, location):
        """Take a 2 finger images and template it, then store in 'location'"""
        for fingerimg in range(1, 3):
            if fingerimg == 1:
                print("Place finger on sensor...", end="")
            else:
                print("Place same finger again...", end="")

            while True:
                i = self.finger.get_image()
                if i == adafruit_fingerprint.OK:
                    print("Image taken")
                    break
                if i == adafruit_fingerprint.NOFINGER:
                    print(".", end="")
                elif i == adafruit_fingerprint.IMAGEFAIL:
                    print("Imaging error")
                    self.finger_enrolled_signal.emit(False)
                    return False
                else:
                    print("Other error")
                    self.finger_enrolled_signal.emit(False)
                    return False

            print("Templating...", end="")
            i = self.finger.image_2_tz(fingerimg)
            if i == adafruit_fingerprint.OK:
                print("Templated")
            else:
                if i == adafruit_fingerprint.IMAGEMESS:
                    print("Image too messy")
                elif i == adafruit_fingerprint.FEATUREFAIL:
                    print("Could not identify features")
                elif i == adafruit_fingerprint.INVALIDIMAGE:
                    print("Image invalid")
                else:
                    print("Other error")
                self.finger_enrolled_signal.emit(False)
                return False

            if fingerimg == 1:
                print("Remove finger")
                time.sleep(1)
                while i != adafruit_fingerprint.NOFINGER:
                    i = self.finger.get_image()

        print("Creating model...", end="")
        i = self.finger.create_model()
        if i == adafruit_fingerprint.OK:
            print("Created")
        else:
            if i == adafruit_fingerprint.ENROLLMISMATCH:
                print("Prints did not match")
            else:
                print("Other error")
            self.finger_enrolled_signal.emit(False)
            return False

        print("Storing model #%d..." % location, end="")
        i = self.finger.store_model(location)
        if i == adafruit_fingerprint.OK:
           
            print("Stored")
        else:
            if i == adafruit_fingerprint.BADLOCATION:
                print("Bad storage location")
               
            elif i == adafruit_fingerprint.FLASHERR:
                print("Flash storage error")
                
            else:
                print("Other error")
            self.finger_enrolled_signal.emit(False)
            return False
        self.finger_enrolled_signal.emit(True)
        return True


    def save_fingerprint_image(self, filename):
        """Scan fingerprint then save image to filename."""
        print("Place finger on sensor...", end="")
        while True:
            i = self.finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        # let PIL take care of the image headers and file structure
        from PIL import Image  # pylint: disable=import-outside-toplevel

        img = Image.new("L", (192, 192), "white")
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
            if x == 191:
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

    def check_print(self, id_num):
        self.finger.set_led(color=3, mode=1)
        if self.get_fingerprint():
            print("Detected #", self.finger.finger_id, "with confidence", self.finger.confidence)
            if self.finger.finger_id == id_num:
                self.finger_auth_signal.emit(True)
                print("Auth Success")
            else:
                self.finger_auth_signal.emit(True)
        else:
            print("Finger not found")
            self.finger_auth_signal.emit(True)



    # initialize LED color
    # led_color = 1
    # led_mode = 3
    # while True:
    #     # Turn on LED
    #     finger.set_led(color=led_color, mode=led_mode)
    #     print("----------------")
    #     if finger.read_templates() != adafruit_fingerprint.OK:
    #         raise RuntimeError("Failed to read templates")
    #     print("Fingerprint templates: ", finger.templates)
    #     if finger.count_templates() != adafruit_fingerprint.OK:
    #         raise RuntimeError("Failed to read templates")
    #     print("Number of templates found: ", finger.template_count)
    #     if finger.read_sysparam() != adafruit_fingerprint.OK:
    #         raise RuntimeError("Failed to get system parameters")
    #     print("Size of template library: ", finger.library_size)
    #     print("e) enroll print")
    #     print("f) find print")
    #     print("d) delete print")
    #     print("s) save fingerprint image")
    #     print("r) reset library")
    #     print("l) set LED")
    #     print("q) quit")
    #     print("----------------")
    #     c = input("> ")
    #
    #     if c == "l":
    #         c = input("color(r,b,p anything else=off)> ")
    #         led_mode = 3
    #         if c == "r":
    #             led_color = 1
    #         elif c == "b":
    #             led_color = 2
    #         elif c == "p":
    #             led_color = 3
    #         else:
    #             led_color = 1
    #             led_mode = 4
    #     elif c == "e":
    #         enroll_finger(get_num(finger.library_size))
    #     elif c == "f":
    #         # breathing LED
    #         finger.set_led(color=3, mode=1)
    #         if get_fingerprint():
    #             print("Detected #", finger.finger_id, "with confidence", finger.confidence)
    #         else:
    #             print("Finger not found")
    #     elif c == "d":
    #         if finger.delete_model(get_num(finger.library_size)) == adafruit_fingerprint.OK:
    #             print("Deleted!")
    #         else:
    #             print("Failed to delete")
    #     elif c == "s":
    #         if save_fingerprint_image("fingerprint.png"):
    #             print("Fingerprint image saved")
    #         else:
    #             print("Failed to save fingerprint image")
    #     elif c == "r":
    #         if finger.empty_library() == adafruit_fingerprint.OK:
    #             print("Library empty!")
    #         else:
    #             print("Failed to empty library")
    #     elif c == "q":
    #         print("Exiting fingerprint example program")
    #         # turn off LED
    #         finger.set_led(mode=4)
    #         raise SystemExit
    #     else:
    #         print("Invalid choice: Try again")