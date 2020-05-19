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
from BLEach_man_id import MANUFACTURERS
from BLEach_man_id import MAN_MAX_ID

class bleDevice:

	# constructor
	def __init__(self):
		# initialize internal variables
		self.name = "NotSet"
		self.rssi = 0
		self.address = "xx:xx:xx:xx:xx:xx"
		self.channel = -1
		self.connectable = False
		self.servUUID = list(())
		self.txPower = -1
		self.data = None
		self.advData = None
		self.appleData = None
		self.peripheral = None
		self.advApplePuckType = -1
		self.manufacturer = "<notset>"
		self.man_id = -1

	def setData(self, data):
		self.data = data

	def getData(self):
		return self.data

	def setAdvData(self, data ):
		self.advData = data
		tmpdata = data
		man_name = "<no man data>"
		# see if we can decode the actual manufacturer ID
		if data is not None:
			self.man_id = int.from_bytes(data[0:2], byteorder="little")
			# see if we can find it in the list
			if( self.man_id > MAN_MAX_ID ):
				man_name = "<not in range>"
			else:
				man_name = MANUFACTURERS.get(self.man_id, MANUFACTURERS.get(0xFFFF, "FAILED"))
				# offset the manufacturers data by the vendor ID code
				tmpdata = bytes(data[2:])

			self.advData = tmpdata
			self.manufacturer = man_name

	def getAdvData(self):
		return self.advData

	def getManufID(self):
		return self.man_id
	
	def setAppleData(self, data ):
		self.appleData = data

	def getAppleData(self):
		return self.appleData

	def setApplePuckType(self, id):
		self.advApplePuckType = id
		if( id > 0 ):
			# this is probably an Apple device
			self.manufacturer = "Apple ???"

	def getApplePuckType(self):
		return self.advApplePuckType

	def setManufacturer(self, manufac):
		self.manufacturer = manufac

	def getManufacturer(self):
		return self.manufacturer
	
	def setTxPower(self, power):
		self.txPower = power
	
	def getTxPower(self):
		return self.txPower

	def setServiceIDs(self, uuids):
		self.servUUID = uuids
	
	def getServiceIDs(self):
		return self.servUUID

	def getServiceIDs_asStr(self):
		retStr = ""
		if(len(self.servUUID) == 0):
			retStr += "<none>"
		else:
			retStr = ""
			for x in self.servUUID:
				retStr += str(x)
				retStr += ", "
		return retStr

	def setConnectable(self, cnct):
		self.connectable = cnct

	def isConnectable(self):
		return self.connectable

	def setChannel(self, chan):
		self.channel = chan
	
	def getChannel(self):
		return self.channel

	def setPeripheral(self, periph):
		self.peripheral = periph
	
	def getPeripheral(self):
		return self.peripheral

	def setName(self, name ):
		self.name = str(name)

	def getName(self):
		return str(self.name)

	def setRSSI(self, rssi ):
		self.rssi = rssi 

	def getRSSI(self):
		return self.rssi
	
	def setAddress(self, addr ):
		self.address = addr

	def getAddress(self):
		return self.address