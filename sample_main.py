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

# initilize the BLE module
if( bleach.setDebug( True, False) == False ):
	print("[MAIN - ERROR] Unable to set debug flags???")

if( bleach.load() == True ):
	print("[MAIN] BLEach module loaded successfully")
else:
	print("[MAIN - ERROR] BLEach module load failed")

# let's run a discover and see what we find
myDevs = bleach.discover()
if( len(myDevs) ) > 0:
	print("[MAIN] Discovered "+str(len(myDevs))+" devices")
	for x in myDevs:
		print(x.name)
else:
	print("[MAIN] No BLE devices found")
