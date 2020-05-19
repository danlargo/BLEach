#
# BLEach - Clean new approach to BLE wrapper for python
#
# (c) copyright 2020 - Slapfrog Labs (https://danlargo.com/slapfrog-labs/)
#
# Licensed under the GNU General Public License v3.0 (https://github.com/danlargo/BLEach/blob/master/LICENSE)
#
# Module Name - bleach.py
#
# Author : Stephen Davis, P.Eng
#
# Description : main module entry point
#
FAILDEP = True
LOADED = False
DEBUG=False
# load system dependencies
try:
	import sys
	import subprocess
	import asyncio
	import time
	import os
	import platform

except Exception as err:
    print("----IMPORT FAILURE---------------------\n"+
	"[FATAL] "+str(err)+
    "[FATAL] Unable to Load BLEach module as it needs <time> <sys> <subprocess> <asyncio> <libdispatch> <os> <platform> modules to self install\n"+
    "[FATAL] run: pip3 install <module name> and then try to import <bleach> again\n"+
    "--------------------------------------------\n")
    quit()

# load local dependencies
try:
	import ver
	import bleachDevice as dev
	import cbmanagerDelegate
	import helpers
	FAILDEP = False

except Exception as err:
	print("----IMPORT FAILURE---------------------\n"+
	"[Confused] "+str(err)+"\n"+
	"[Confused] Unable to Load BLEach module as it needs these local modules to operate\n"+
	"[Confused] <ver> <CoreBluetooth> <bleachDevice> <belDelegate> <helpers>\n"+
	"[Confused] This implies an install error\n"+
	"--------------------------------------------\n")
	quit()

# other flags
OSTAG = ""

#--------------------
# METHOD : setDebug - turns debugging logging on and off (pass through to set helper flags)
# Parameters :
#	onOrOff = turn debugging on or off
#	logOnly = turns off console printing (logOnly = True, turns off console logging, print to console is default) 
# 
# Return Value :
#	None
#--------------------
#
def setDebug( onOrOff, logOnly=False ):
	return( helpers.setDEBUG( onOrOff, logOnly ) )

#--------------------
# METHOD : getVersion - returns development version of the BLEach module
# Parameters :
#	printVer = prints the version to the console in addition to returning as a string, default is to return string only
#
# Return Value :
#	version - <str>
#--------------------
#
def getVersion( printVer=False ):
	verStr = ver.getVer()
	if( printVer == True ):
		print("BLEach (BLE module) v"+verStr)
	return verStr

#--------------------
# METHOD : checkDep - check routine to validate if systems dependencies have been loaded, will try to exit main program
# Parameters :
#	none
#
# Return Value :
#	checkFlag - indicating dependencies have not been validated
#--------------------
#
def checkDep():
	global FAILDEP
	if( FAILDEP == True ):
		print("[FATAL] SYSTEM Dependencies for BLEach are not loaded - Unable to continue - Trying to QUIT()")
		quit()
		return False

	return True

#--------------------
# METHOD : load - sets up and loads all module and library dependencies specific to the BLE processing
# Parameters :
#	none
#
# Return Value :
#	LOADED - global variable indicating dependencies loaded OK
#--------------------
#
def load():
	global OSTAG
	global LOADED

	# do this for every function to ensure user not ignoring dependencies
	if( checkDep() == False ): quit()

	# only run if we have not run it before
	if( LOADED == True ):
		if( DEBUG): helpers.debugMsg("[INFO] BLEach, already loaded - skipping load() call", False)
		return

	# let's assume we get everything loaded OK
	LOADED = True

	# try to load all know dependencies
	helpers.debugMsg("-------------------------")
	helpers.debugMsg("BLEach - v"+ver.getVer()+"-- (c) copyright 2020, developed by Slapfrog Labs")
	helpers.debugMsg("[INFO] ...BLEach evaluating dependencies")

	# find the OS we are on
	OSTAG = helpers.getOS()

	# start loading the system specific dependencies
	if( OSTAG == "MAC" ):
		# CoreBluetooth via PyObjC
		try:
			import CoreBluetooth
			helpers.debugMsg("[INFO] CoreBluetooth (MAC) - imported correctly")
		except Exception as err:
			# try to self install
			helpers.debugMsg("[INSTALL] Attempting to install CoreBluetooth module")
			if( helpers.install("PyObjC") == False ):
				helpers.debugMsg("[FATAL] "+str(err))
				helpers.debugMsg("[FATAL] Unable to Load CoreBluetooth")
				helpers.debugMsg("[FATAL] ...run pip3 install CoreBluetooth")
				helpers.debugMsg("[FATAL] ...then run your prgoram again")
				LOADED = False
			else:
				import CoreBluetooth

	# BLEach dependencies loaded ok
	helpers.debugMsg("[INFO] ...BLEach dependencies loaded OK")

	# evaluate BLE environment


	return LOADED

#--------------------
# METHOD : discover - invoke discover() to grab list of close, detectable BLE devices
# Parameters :
#   devToFind - UUID (on MAC) or BLE addres to find, if None then it returns everything
#	timeout - time in seconds to wait for device advertizements to happen
#   connectableOnly - flag indicating only to return devices that are connectable (ignored if the devToFind info is set)
#
# Return Value :
#	devices - a list of bleachDevices discovered during the listening process
#--------------------
#
def discover(devToFind=None, timeout=2, connectableOnly=False):
	# do this for every function to ensure user not ignoring dependencies
	if( checkDep() == False ): quit()

	devices = list(())

	# check if library is properly loaded yet
	global LOADED
	global DEBUG
	if( LOADED == False ):
		helpers.debugMsg("[WARNING] ...bleach module not loaded, calling bleach.load() now, this should be called at start of main program")
		if( load() == False ):
			helpers.debugMsg("[WARNING] ...bleach module failed to load")
			return None

	# MAC discovery here
	if( OSTAG == "MAC" ):
		try:
			# Using CoreBluetooth
			import CoreBluetooth
			from PyObjCTools import AppHelper

			bleManage = CoreBluetooth.CBCentralManager.alloc()
			if( bleManage is not None ):
				helpers.debugMsg( "[INFO] CBCentralManager loaded OK")
				bleManage.init()
				# create the CBManager Delegate
				myDelegate = cbmanagerDelegate.managerDelegate()
				myDelegate.setTimeout(timeout)
				myDelegate.setParams(connectableOnly, DEBUG)

				bleManage.initWithDelegate_queue_options_(myDelegate, None, None)
				AppHelper.runConsoleEventLoop()

				# grab the device list
				devices = myDelegate.getDevices()

			else:
				helpers.debugMsg("[WARNING] CBCentralManager.alloc() returned <None>")
		except Exception as err:
				helpers.debugMsg("[WARNING] BLEach discover() failed with error <"+str(err)+">")

	# send back the list of devices
	return devices