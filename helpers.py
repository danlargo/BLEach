#
# BLEach - Clean new approach to BLE wrapper for python
#
# (c) copyright 2020 - Slapfrog Labs (https://danlargo.com/slapfrog-labs/)
#
# Licensed under the GNU General Public License v3.0 (https://github.com/danlargo/BLEach/blob/master/LICENSE)
#
# Module Name - helpers.py
#
# Author : Stephen Davis, P.Eng
#
# Description : debug, logging and setup functions
#
DEBUGFILE = None
LOGONLY = True
DEBUGFLAG = False

# load system dependencies
try:
	import time
	import subprocess
except Exception as err:
    print("----IMPORT FAILURE---------------------\n"+
	"[FATAL] "+str(err)+"\n"+
    "[FATAL] Unable to Load BLEach Helper module as it needs\n"+
	"[FATAL] <time> <subprocess> modules to self install\n"+
    "[FATAL] run: pip3 install <module name> and then try to import <bleach> again\n"+
    "--------------------------------------------\n")
    quit()

#--------------------
# METHOD : setDebug - turns debugging logging on and off
# Parameters :
#	onOrOff = turn debugging on or off
#	logOnly = turns off console printing (logOnly = True, turns off console logging, print to console is default) 
# 
# Return Value :
#	None
#--------------------
#
def setDEBUG( onOrOff, logOnly=False ):
	global DEBUGFLAG
	global LOGONLY
	global DEBUGFILE
	DEBUGFLAG = onOrOff
	LOGONLY = logOnly
	if( DEBUGFLAG == True ):
		# open the log file
		try:
			DEBUGFILE = open("bleachDebug.log", mode="a")
			DEBUGFILE.write("BLEach system logger opened at : " + time.asctime( time.localtime(time.time() )) + "\n" )
		except Exception as err:
			DEBUGFILE = None
			return False
	else:
		# close the log file if it is open
		if( DEBUGFILE != None ):
			DEBUGFILE.close()
			DEBUGFILE = None
	
	return True

#--------------------
# METHOD : debugMsg - generic log method, dumps to file if it can open one
# Parameters :
#	msg - message to print
#	justPrint = ignored if debugging is ON, if debugging is OFF then it overrides and prints to console
#
# Return Value :
#	None
#--------------------
#
def debugMsg( msg, justPrint=True ):
	global DEBUGFLAG
	global LOGONLY
	global DEBUGFILE
	# format the message
	localTm = time.asctime( time.localtime(time.time() ) )
	logMsg = localTm + " : "+msg
	if( DEBUGFLAG == True ):
		# check if it is only going to file
		if( LOGONLY == False ):
			# grab the time and date
			print(logMsg)
		# check if we have to echo to file
		if( DEBUGFILE != None ):
			DEBUGFILE.write(logMsg+"\n")
		else:
			print("[DEBUG] DEBUG FILE NOT OPEN")
			print(localTm, " : ", logMsg)
	else:
		# if debug called but no debug is enabled and just print flag is set then send to console anyway
		if( justPrint == True ):
			print(localTm, " : ", logMsg)

#--------------------
# METHOD : install - helper function to self install dependent modules
# Parameters :
#	package = name of package to install
#
# Return Value :
#	success - boolean - flag indicating module was loaded properly
#--------------------
def install(package):
	try:
		debugMsg("[INSTALL] Attempting to Install - " + package, True)
		cmd = "pip3 install " + package
		outLog = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
		debugMsg("[INSTALL] " + package + " Successfully installed", True)
		return True
	except Exception as err:
		debugMsg("[FATAL] " + str(err))
		debugMsg("[FATAL] Failed to Install - " + package, True)
	
	return False
