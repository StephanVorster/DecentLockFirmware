import time
import binascii

from pn532pi import Pn532
from pn532pi import Pn532Hsu
from pn532pi import Pn532I2c
from pn532pi import Pn532Spi
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
import RPi.GPIO as GPIO
import threading
from xrpl_auth import create_transaction_fromtx_blob, is_valid_transaction




class nfc_auth_handler():

	# Set the desired interface to True

	# SPI = True
	# I2C = False
	# HSU = False

	# The xrpl address of this device
	address = "rHEA2cdWLUuoDiWyoxh1bpuNLYLxFug1Yf"
	# The xrpl addresss and public key authorized to open this lock
	authorized_accounts = [{"address":"rhUywgyUBUnTz3xw9VuMPtPggD2xzdbKK6", "pub_key": "EDC964C2CF0B0E9F781781566F7AB05042E1EBFD64AB8376DC1CF847FD4379DAE0" }]
	# account='rhUywgyUBUnTz3xw9VuMPtPggD2xzdbKK6'
	last_sequence = -1
	# sequence=38386169

	#   auth_signal = pyqtSignal(bool)

	setup_complete = False

	state_ready = False

	def __init__(self):

		super().__init__()

		PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
		self.nfc = Pn532(PN532_SPI)
		self.setup()
		self.setup_complete = True

		print("NFC Init")

	def getGenStatusRegiser(self):
		PN532_COMMAND_GETFIRMWAREVERSION    = (0x04)
		if (self.nfc._interface.writeCommand(bytearray([PN532_COMMAND_GETFIRMWAREVERSION]))):
			return 0

		# read data packet
		status, response = self.nfc._interface.readResponse()
		if (status < 0):
			return 0

		# response = self.pn532_packetbuffer[0]
		# response <<= 8
		# response |= self.pn532_packetbuffer[1]
		# response <<= 8
		# response |= self.pn532_packetbuffer[2]
		# response <<= 8
		# response |= self.pn532_packetbuffer[3]

		return int.from_bytes(response, byteorder='big')

	def is_setup_complete(self):
		return self.setup_complete

	# if SPI:
	#     print("SPI")
	#     PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
	#     nfc = Pn532(PN532_SPI)
	# # When the number after #elif set as 1, it will be switched to HSU Mode
	# elif HSU:
	#     print("HSU")
	#     PN532_HSU = Pn532Hsu(Pn532Hsu.RPI_MINI_UART)
	#     nfc = Pn532(PN532_HSU)

	# # When the number after #if & #elif set as 0, it will be switched to I2C Mode
	# elif I2C:
	#     print("I2C")
	#     PN532_I2C = Pn532I2c(1)
	#     nfc = Pn532(PN532_I2C)
	#     nfc.begin()

	def setup(self):
		print("-------Peer to Peer HCE--------")

		self.nfc.begin()

		versiondata = self.nfc.getFirmwareVersion()
		if not versiondata:
			for i in range(0, 3):
				versiondata = self.nfc.getFirmwareVersion()
			if not versiondata:
				print("Didn't find PN53x board")
				raise RuntimeError("Didn't find PN53x board")  # halt

		# Got ok data, print it out!
		print("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF, (versiondata >> 16) & 0xFF,
																	(versiondata >> 8) & 0xFF))

		# Set the max number of retry attempts to read from a card
		# This prevents us from waiting forever for a card, which is
		# the default behaviour of the PN532.
		self.nfc.setPassiveActivationRetries(0xFF)

		# self.nfc.writeRegister(0xA8, 0b11111111)
		# self.nfc.writeRegister(0xE8, 0b10111101)
		# self.nfc.writeRegister(0xD3, 0b11111000)



		# configure board to read RFID tags
		self.nfc.SAMConfig()


	def get_auth1(self, counter=0):
		print("Attemping to get Autthentication")
		apdu_string = f"{{'address': '{self.address}'}}"
		apdu = bytearray(apdu_string.encode())
		success, back = self.send_data(apdu)
		ret_str = None
		counter += 1
		cont_flag = True
		if (success):
			if(back.decode() == "ACK"):
				while cont_flag:
					counter += 1
					print("HERE")
					success, back = self.send_data(apdu)
					print("responseLength: {:d}", len(back))
					print(f"Message: {back}")
					if counter>= 3:
						cont_flag = False
						# if back.decode() != "ACK":
						#   cont_flag = False
					if back.decode() != "ACK":
						ret_str = back.decode()
						cont_flag = False
			else:
				ret_str = back.decode()
		return ret_str


	def get_authx(self, auth_number, counter=0):
		print("Attemping to get Autthentication")
		apdu_string = f"{{'action': 'auth_blob_{auth_number}'}}"
		apdu = bytearray(apdu_string.encode())
		success, back = self.send_data(apdu)
		ret_str = None
		counter += 1
		cont_flag = True
		if (success):
			if(back.decode() == "ACK"):
				while cont_flag:
					success, back = self.send_data(apdu)
					print("responseLength: {:d}", len(back))
					print(f"Message: {back}")
					if counter>= 3:
						if back.decode() != "ACK":
							cont_flag = False
					if back.decode() != "ACK":
						ret_str = back.decode()
						cont_flag = False
			else:
				ret_str = back.decode()
		return ret_str


	def send_data(self, data):
		success, response = self.nfc.inDataExchange(data)
		i = 0
		if not success:
			print("Initial Connection failed")
		retries = 8
		for i in range(0, retries):
			print("Retrying Connection")
			success, response = self.nfc.inDataExchange(data)
			if success:
				break
			# time.sleep(0.2)
		if i >= retries and not success:
			print("Connection failed")

		return success, response


	def send_nfc_apdu_hello(self):
		print("Found something!")

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

		return success, response








	def is_valid_accout(self, address, pub_key):
		"""
		This function checks if the address and public key provided are in the authorized accounts 
		which are authorized to open this lock. The account address and the public key have to be in 
		the same entry, this prevents frudulant attempts to open the lock with a mix match of accounts 
		and keys
		"""
		for i in range(0, len(self.authorized_accounts)):
			valid_account = False
			valid_pub_key =False
			if address == self.authorized_accounts[i]["address"]:
				valid_account = True
			if pub_key == self.authorized_accounts[i]["pub_key"]:
				valid_pub_key = True
			if valid_pub_key and valid_account:
				return True

		return False

	

	def setStateReady(self, state:bool):
		self.state_ready = state
		return


	def search_for_device(self):
		"""
		In the UI integration the while should be preceded by a system wide enabled variable which will disable the nfc field when needed to save power
		"""
		success = False
		while not success:
			success = self.nfc.inListPassiveTarget()
		return success
	
	def nfc_auth_coms(self):
		tx_blob = []
		auth_1 = self.get_auth1()
		if auth_1 is not None:
			tx_blob.append(auth_1)
			auth1_success = True
			print(auth_1)
		else:
			print("Auth 1 Failed try again")
			return None
		if auth1_success:
			auth_2 = self.get_authx(auth_number=2)
			if auth_2 is not None:
				tx_blob.append(auth_2)
				auth2_success = True
				print(auth_2)
			else:
				print("Auth 2 Failed try again")
				return None
		if auth2_success:
			auth_3 = self.get_authx(auth_number=3)
			if auth_3 is not None:
				tx_blob.append(auth_3)
				auth3_success = True
				return tx_blob
			else:
				print("Auth 3 Failed try again")
				return None
	
	def authenticate_msg(self, tx_blob):
		tzac = create_transaction_fromtx_blob(tx_blob)
		authorized_account = self.is_valid_accout(tzac.account, tzac.signing_pub_key)
		if authorized_account:
			valid = is_valid_transaction(tx_blob)
			if valid:
				authenticated = True
				print(tzac.sequence)

				return True
			else:
				print("Tx blob not valid")
				
				return False
		else:
			print("Account not authorized to open lock")
			return False



	def main_nfc_thread(self):
		"""
		In the UI integration the while should be preceded by a system wide enabled variable which will disable the nfc field when needed to save power
		"""

		while 1:
			authenticated = False
			success = self.search_for_device()
			if success:
				print("Found it")
				success, response = self.send_nfc_apdu_hello()
				
				tx_blob = self.nfc_auth_coms()
				if tx_blob is not None:
					tx_blob = "".join(tx_blob)
					authenticated = self.authenticate_msg(tx_blob=tx_blob)
					
			else:
				if response != b"9000":
					print("Phone might be locked or might be rfid")
				else:
					print("Might be RFID")
			if authenticated:
				#   if self.state_ready:
					#     self.auth_signal.emit(False)
				print("AUTHENTICATED")
			else:
				print("ACCESS DENIED")



if __name__ == '__main__':

	test_nfc = nfc_auth_handler()
	def cb2(state):
		print(state, "State")

	def cb(state):
		# test_nfc.auth()
		print("INTERRUPT 17")

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17, GPIO.IN)
	GPIO.add_event_detect(17, GPIO.FALLING, callback=cb)
	val = 0
	prev = 0

	test_nfc.setStateReady(True)
	t1 = threading.Thread(target=test_nfc.main_nfc_thread, name="NFC:1")
	t1.start()
	t1.join()

  


    

    