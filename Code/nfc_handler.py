import sys
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtCore import QObject, Signal, Slot, QTimer
import binascii
from pn532pi import Pn532
from pn532pi import Pn532Spi
import codecs
from xrpl_auth_lite import is_valid_transaction

class nfcHandler(QObject):

    nfc_module_active = False
    PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
    nfc = Pn532(PN532_SPI)


    def __init__(self, parent=None):
        super().__init__(parent)
        # Get the nfc module's version data to see if the module has a valid hardware connection
        version_data = self.nfc.getFirmwareVersion()
        if not version_data:
            # if the module's firmware version could not be found try 3 more times.
            for i in range(0, 3):
                version_data = self.nfc.getFirmwareVersion()
                if version_data:
                    self.nfc_module_active = True
                    break
        else:
            self.nfc_module_active = True
        # Init the Secure Access Module on the PN532
        self.nfc.SAMConfig()
        self.nfc.setPassiveActivationRetries(0xFF)
        if self.nfc_module_active:
            self.timer = QTimer()
            self.timer.timeout.connect(self.handle_connect)
            self.timer.start(500)

    def send_data(self, data):
        success, response = self.nfc.inDataExchange(data)
        i = 0
        if not success:
            print("Initial Connection failed")
        retries = 32
        for i in range(0, retries):
            print("Retrying Connection")
            success, response = self.nfc.inDataExchange(data)
            if success:
                break
            # time.sleep(0.2)
        if i >= retries and not success:
            print("Connection failed")

        return success, response

    def handle_connect(self):
        success = self.nfc.inListPassiveTarget()

        if (success):

            print("Found something!")
            self.timer.stop()
            selectApdu = bytearray([0x00,
                                    0xA4,
                                    0x04,
                                    0x00,
                                    0x07,
                                    0xA0,
                                    0x00,
                                    0x00,
                                    0x02,
                                    0x47,
                                    0x10,
                                    0x01
                                    ])

            success, response = self.send_data(selectApdu)

            if (success):

                # print("responseLength: {:d}", len(response))
                print(binascii.hexlify(response))
                print(f"Response: {response}")

                while (success):
                    apdu = bytearray(b"{'action': 'auth_blob_1'}")
                    success, back = self.send_data(apdu)

                    if (success):
                        print("responseLength: {:d}", len(back))
                        # tx_blob = codecs.decode(binascii.hexlify(back), 'utf-8')
                        tx_blob = codecs.decode(back, 'utf-8')
                        # codecs.decode(gzip.decompress(back), 'utf-8')
                        # print(f"Tx Blob: {codecs.decode(back, 'utf-8')}")
                        # print(f"Is valid transaction: {is_valid_transaction(tx_blob)}")
                        print("Received blob part 1")
                        apdu = bytearray(b"{'action': 'auth_blob_2'}")
                        success, back = self.send_data(apdu)
                        if success:
                            tx_blob += codecs.decode(back, 'utf-8')
                            print("Received blob part 1")
                            # print(tx_blob)
                            apdu = bytearray(b"{'action': 'auth_blob_3'}")
                            success, back = self.send_data(apdu)
                            if success:
                                tx_blob += codecs.decode(back, 'utf-8')
                                print(tx_blob)
                                print(f"Is valid transaction: {is_valid_transaction(tx_blob)}")
                                self.timer.start(500)
                                return False
                    else:
                        print("Broken connection?")
                        self.timer.start(500)
            else:
                print("Failed sending SELECT AID")
                self.timer.start(500)






