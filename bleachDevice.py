#
# BLEach - Clean new approach to BLE wrapper for python
#
# (c) copyright 2020 - Slapfrog Labs (https://danlargo.com/slapfrog-labs/)
#
# Licensed under the GNU General Public License v3.0 (https://github.com/danlargo/BLEach/blob/master/LICENSE)
#
# Module Name - bleachDevice.py
#
# Author : Stephen Davis, P.Eng
#
# Description : device object for BLE devices and sensors found by discover method
#
class bleDevice:

	# constructor
	def __init__(self):
		# initialize internal variables
		self.name = "Unknown"
		self.rssi = 0
		self.address = "00:00:00:00:00:00"

