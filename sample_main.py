#
# BLEach - Clean new approach to BLE wrapper for python
#
# (c) copyright 2020 - Slapfrog Labs (https://danlargo.com/slapfrog-labs/)
#
# Licensed under the GNU General Public License v3.0 (https://github.com/danlargo/BLEach/blob/master/LICENSE)
#
# Module Name - main.py
#
# author : Stephen Davis, P.Eng
#
# Description : sample code to demonstrate the use of the BLEach module
#
print("------------------------------------")
print("BLEach (BLE python module) Demo Code")
print("------------------------------------")

import bleach
from bleachDevice import bleDevice 

# initilize the BLE module debug state
if( bleach.setDebug(False, False) == False ):
	print("[setDebug()] Unable to set debug flags???")

if( bleach.load() == False ):
	print("[load()] BLEach module load failed - Exiting")
	quit()

# let's run a discover for 10 seconds and see what we find
myDevs = bleach.discover(None, 10, False)
if( len(myDevs) ) > 0:
	print("[discover()] Discovered "+str(len(myDevs))+" devices")
	for x in myDevs:
		print("[discover()] ", x.getName(), " - ", x.getManufacturer(), ", ", x.getManufID(),
			"\n(rssi:", x.getRSSI(), " chan: ", x.getChannel(), " pwr: ", x.getTxPower(),
			"\n[ID] ", x.getAddress(),
			"\n[CanConnect] ", x.isConnectable(),
			"\n[UUID List]", x.getServiceIDs_asStr(),
			"\n[AdvData] ", x.getAdvData(), 
			"\n[AppleData]", x.getApplePuckType(),
			"\n"
		)
	
	# debug dump
	#print("--------\n-------\n---DEBUG---")
	#for x in myDevs:
		# dump the data dictionary
	#	print(x.getData().items())
	#	print(x.getPeripheral())
else:
	print("[discover()] No BLE devices found")
