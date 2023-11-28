import json
import time
import binascii
from time import sleep
from pn532pi import Pn532
from pn532pi import Pn532Hsu
from pn532pi import Pn532I2c
from pn532pi import Pn532Spi
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
import RPi.GPIO as GPIO
import threading
from xrpl_auth import create_transaction_fromtx_blob, is_valid_transaction
import os
import subprocess


class nfc_auth_handler():
	# Set the desired interface to True

	# SPI = True
	# I2C = False
	# HSU = False
	AUTH_STATE = "AUTH"
	ONBOARD_STATE = "ONBOARD"
	reset_pin = 17
	state = AUTH_STATE
	debug = False
	# The xrpl address of this device
	address = "rHEA2cdWLUuoDiWyoxh1bpuNLYLxFug1Yf"
	# The xrpl addresss and public key authorized to open this lock
	authorized_accounts = [{"address": "rhUywgyUBUnTz3xw9VuMPtPggD2xzdbKK6",
							"pub_key": "EDC964C2CF0B0E9F781781566F7AB05042E1EBFD64AB8376DC1CF847FD4379DAE0"}]

	last_sequence = -1
	# sequence=38386169

	#   auth_signal = pyqtSignal(bool)

	setup_complete = False

	state_ready = False

	def __init__(self, debug):

		super().__init__()
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.reset_pin, GPIO.OUT)
		GPIO.output(self.reset_pin, GPIO.HIGH)
		PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
		self.nfc = Pn532(PN532_SPI)
		self.setup()
		self.debug = debug
		self.setup_complete = True

		print("NFC Init")

	def is_setup_complete(self):
		return self.setup_complete

	def setup(self):
		print("-------Peer to Peer HCE--------")

		self.nfc.begin()

		self.check_and_reset()

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
		print("Sending Lock Address")
		apdu_string = f"{{'address': '{self.address}'}}"
		apdu = bytearray(apdu_string.encode())
		success, back = self.send_data(apdu)
		sleep(0.01)
		ret_str = None
		counter += 1
		cont_flag = True
		if (success):
			if (back.decode() == "ACK"):
				while cont_flag:
					counter += 1
					print("HERE")
					success, back = self.send_data(apdu)
					print("responseLength: {:d}", len(back))
					print(f"Message: {back}")
					if counter >= 3:
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
			if (back.decode() == "ACK"):
				while cont_flag:
					success, back = self.send_data(apdu)
					print("responseLength: {:d}", len(back))
					print(f"Message: {back}")
					if counter >= 3:
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
		retries = 6
		for i in range(0, retries):
			print("Retrying Connection")
			success, response = self.nfc.inDataExchange(data)
			if success:
				break
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

	def edit_wifi_config(self, ssid, password):
		# interface = 'wlan0'
		# name = ssid
		# password = password
		# print("Attemping to edit wifi config")
		# cmd = f"iwconfig {interface} essid {name} key {password}"
		# os.system('iwconfig ' + interface + ' essid ' + name + ' key ' + password)

		# print("Attemping to edit wifi config")
		# config_lines = [
		# 	'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
		# 	'update_config=1',
		# 	'country=US',
		# 	'\n',
		# 	'network={',
		# 	'\tssid="{}"'.format(ssid),
		# 	'\tpsk="{}"'.format(password),
		# 	'}\n'
		# ]
		# config = '\n'.join(config_lines)
		# print("Attempting first command")
		# # give access and writing. may have to do this manually beforehand
		# os.system("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")
		# print("Attempting to edit config file")
		# # writing to file
		# with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
		# 	wifi.write(config)

		# print("Wifi config added. Refreshing configs")
		# ## refresh configs
		# os.system("sudo wpa_cli -i wlan0 reconfigure")

		# Update /etc/wpa_supplicant/wpa_supplicant.conf
		with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as f:
			f.write('\n\nnetwork={\n')
			f.write(f'    ssid="{ssid}"\n')
			f.write(f'    psk="{password}"\n')
			f.write('}\n')

		# Update /etc/network/interfaces
		with open('/etc/network/interfaces', 'a') as f:
			f.write('\n\nauto wlan0\n')
			f.write('iface wlan0 inet dhcp\n')
			f.write('wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf\n')

		# Restart networking
		subprocess.run(['sudo', 'systemctl', 'restart', 'networking'])

	def onboarding_get_xrpl_address(self):
		apdu_string = f"{{'onboard': '{self.address}'}}"
		apdu = bytearray(apdu_string.encode())
		success, response = self.send_data(data=apdu)
		if success:
			# return response.decode()
			print(response.decode())
			js_obj = json.loads(response.decode())
			print(type(response.decode()))

			return json.loads(response.decode())["ADDR"]
		return None

	def onboarding_get_SSID(self):
		apdu_string = f"{{'onboard': 'SSID'}}"
		apdu = bytearray(apdu_string.encode())
		success, response = self.send_data(data=apdu)
		if success:
			# return response.decode()
			print(response.decode())
			return json.loads(response.decode())["SSID"]
		return None

	def onboarding_get_wifi_pass(self):
		apdu_string = f"{{'onboard': 'PASS'}}"
		apdu = bytearray(apdu_string.encode())
		success, response = self.send_data(data=apdu)
		if success:
			print(response.decode())
			return json.loads(response.decode())["PASS"]
		# return response.decode()
		return None

	def onboarding_get_pub_key(self):
		apdu_string = f"{{'onboard': 'KEY'}}"
		apdu = bytearray(apdu_string.encode())
		success, response = self.send_data(data=apdu)
		if success:
			print(response.decode())
			return json.loads(response.decode())["KEY"]
		# return response.decode()
		return None

	def onboarding_get_token_id(self):
		apdu_string = f"{{'onboard': 'TOKEN'}}"
		apdu = bytearray(apdu_string.encode())
		success, response = self.send_data(data=apdu)
		if success:
			print(response.decode())
			return json.loads(response.decode())["TOKEN"]
		# return response.decode()
		return None

	def onboard_new_device(self):
		onboard_obj = {}

		print("Starting Onboarding")
		address = self.onboarding_get_xrpl_address()
		print(f"Onboarding Address: {address}")
		if address is not None:
			onboard_obj["address"] = address
			print("Onboarding: Getting SSID")
			ssid = self.onboarding_get_SSID()
			if ssid is not None:
				onboard_obj["ssid"] = ssid
				passwd = self.onboarding_get_wifi_pass()
				if passwd is not None:
					onboard_obj["passwd"] = passwd
					pub_key = self.onboarding_get_pub_key()
					if pub_key is not None:
						onboard_obj["pub_key"] = pub_key
						token_id = self.onboarding_get_token_id()
						if token_id is not None:
							onboard_obj["token_id"] = token_id
							self.process_onboarding_obj(onboard_obj)
						else:
							print("Onboarding failed: Receiving Token ID")
					else:
						print("Onboarding failed: Receiving Public Key")
				else:
					print("Onboarding failed: Receiving Wifi Pass")
			else:
				print("Onboarding failed: Receiving SSID")
		else:
			print("Onboarding failed: Receiving XRPL Address")

	def process_onboarding_obj(self, onboarding_obj):
		# self.edit_wifi_config(onboarding_obj["ssid"], onboarding_obj["passwd"])
		account_dict = {}
		account_details_dict = {"pub_key": onboarding_obj["pub_key"], "token_id": onboarding_obj["token_id"]}
		if not os.path.exists("verified_accounts.json"):
			account_dict[onboarding_obj["address"]] = account_details_dict
			with open('verified_accounts.json', 'w') as fp:
				json.dump(account_dict, fp)
		else:
			existing_account_dict = None
			# Read the current accounts file tto the existing_account_dict variable
			with open('verified_accounts.json', 'r') as json_file:
				existing_account_dict = json.loads(json_file.read())
			# Append the new account to the document and overwrite the file with the new address appended
			if existing_account_dict is not None:
				# If the account is not already in the verified accounts file
				if onboarding_obj["address"] not in existing_account_dict.keys():
					existing_account_dict[onboarding_obj["address"]] = account_details_dict
					with open('verified_accounts.json', 'w') as fp:
						json.dump(existing_account_dict, fp)




	def is_valid_accout(self, address, pub_key):
		"""
		This function checks if the address and public key provided are in the authorized accounts
		which are authorized to open this lock. The account address and the public key have to be in
		the same entry, this prevents fraudulent attempts to open the lock with a mix match of accounts
		and keys
		"""
		for i in range(0, len(self.authorized_accounts)):
			valid_account = False
			valid_pub_key = False
			if address == self.authorized_accounts[i]["address"]:
				valid_account = True
			if pub_key == self.authorized_accounts[i]["pub_key"]:
				valid_pub_key = True
			if valid_pub_key and valid_account:
				return True

		return False

	def setStateReady(self, state: bool):
		self.state_ready = state
		return

	def search_for_device(self):
		"""
		In the UI integration the while should be preceded by a system wide enabled variable which will disable the nfc field when needed to save power
		"""
		success = False
		while not success:
			self.check_and_reset()
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

	def checkDeviceConnection(self):
		"""
		This function checks whether the board has a valid SPI connection by requesting the firmware version over SPI.
		If the version isn't found the first time 3 retries will be made, if the device still isn't found, the function returns false.
		If the firmware version is found at all the function returns true
		"""
		versiondata = self.nfc.getFirmwareVersion()
		if not versiondata:
			for i in range(0, 3):
				versiondata = self.nfc.getFirmwareVersion()
			if not versiondata:
				if self.debug:
					print("Didn't find PN53x board")
				return False
		if versiondata:
			if self.debug:
				print("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF,
																			(versiondata >> 16) & 0xFF,
																			(versiondata >> 8) & 0xFF))
		return True

	def resetPn532(self):
		"""
		This function performs a reset of the PN532 module, by pulling the reset pin on the board low
		for a millisecond and rerunning the setup process, this is needed as sometimes the board enters
		an error state and cannot perform any tasks.
		"""
		if self.debug:
			print("Resetting device")
		GPIO.setmode(GPIO.BCM)
		# Set reset pin as output

		GPIO.output(self.reset_pin, GPIO.LOW)
		sleep(0.001)
		GPIO.output(self.reset_pin, GPIO.HIGH)
		self.state_ready = False
		self.setup()
		self.state_ready = True

	def check_and_reset(self):
		connected_no_errors = self.checkDeviceConnection()
		if not connected_no_errors:
			self.resetPn532()

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
				if success and response == b"9000":
					tx_blob = self.nfc_auth_coms()
					if tx_blob is not None:
						tx_blob = "".join(tx_blob)
						authenticated = self.authenticate_msg(tx_blob=tx_blob)

				else:
					if response != b"9000":
						if "onboard" in response.decode():
							print("Starting Onboarding")
							self.onboard_new_device()
						else:
							if self.state_ready:
								self.auth_signal.emit(True)
							print("Phone might be locked or might be rfid")
					else:
						if self.state_ready:
							self.auth_signal.emit(True)
						print("Might be RFID")
				if authenticated:
					if self.state_ready:
						self.auth_signal.emit(True)
					print("AUTHENTICATED")
				else:
					if self.state_ready:
						self.auth_signal.emit(True)
					print("ACCESS DENIED")
					sleep(1)
			else:
				sleep(0.1)


def test_process_onboarding():
	test_nfc = nfc_auth_handler(debug=True)
	test_obj = {"address": "address", "pub_key": "publicKey", "token_id": "token123"}
	test_nfc.process_onboarding_obj(test_obj)

if __name__ == '__main__':
	
	
	# test_nfc = nfc_auth_handler(debug=False)
	# test_nfc.setStateReady(True)
	# t1 = threading.Thread(target=test_nfc.main_nfc_thread, name="NFC:1")
	# t1.start()
	# t1.join()
	test_process_onboarding()
	print("Finished")
