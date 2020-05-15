#
# BLEach - Clean new approach to BLE wrapper for python
#
# (c) copyright 2020 - Slapfrog Labs (https://danlargo.com/slapfrog-labs/)
#
# Licensed under the GNU General Public License v3.0 (https://github.com/danlargo/BLEach/blob/master/LICENSE)
#
# Module Name - ver.py
#
# author : Stephen Davis, P.Eng
#
# Description : project version tracker
#
MAJ_VER = 0
MIN_VER = 1
SUB_VER = 12

# return the version number
def getVer():
	retstr = str(MAJ_VER)+"."+str(MIN_VER).zfill(2)+"."+str(SUB_VER).zfill(4)
	return retstr