#
# BLEach - Clean new approach to BLE wrapper for python
#
# (c) copyright 2020 - Slapfrog Labs (https://danlargo.com/slapfrog-labs/)
#
# Licensed under the GNU General Public License v3.0 (https://github.com/danlargo/BLEach/blob/master/LICENSE)
#
# Module Name - build_man_id_list.py
#
# Author : Stephen Davis, P.Eng
#
# Description : buidl script for the Manufacturing list
#
# - download from https://www.bluetooth.com/specifications/assigned-numbers/company-identifiers/ by selecting and copying the raw list in text, will look like...
# 2269 	0x08DD 	code-Q
# 2268 	0x08DC 	SHENZHEN AUKEY E BUSINESS CO., LTD
# 2267 	0x08DB 	Tertium Technology
# .....
#
# - copy existing data file to <MAN__ID_RAW.old> to preserve
# - save updated manufacturer data to <MAN_ID_RAW.dat>
# - run <build_man_id_list.py> (will access the MAN_ID_RAW.dat file by default)
# - copy the resulting file up one folder and overwrite existing file, format should be...
#
# MANUFACTURERS = {
#    0x0000: "Ericsson Technology Licensing",
#    0x0001: "Nokia Mobile Phones",
#    0x0002: "Intel Corp.",
#    0x0003: "IBM Corp.",
#    0x0004: "Toshiba Corp.",
#    0x0005: "3Com",
#    ...
#    }
#
import time

# welcome the user
print("---\n[BUILD_MAN_ID_File] <build_man_id_list.py - (c) 2020 by Slapfrog Labs, All Rights Reserved")
print("[BUILD_MAN_ID_File] Welcome")

# open data file for writing
print("[BUILD_MAN_ID_File] Attempting to open input file for reading <MAN_ID_RAW.dat>")
try:
    fidIn = open("MAN_ID_RAW.dat", "r")
except Exception as err:
    print("[BUILD_MAD_ID_File - FATAL] ", str(err))
    print("[BUILD_MAD_ID_File - FATAL] Open error on input file, make sure <MAN_ID_RAW.dat> exists in the current folder")
    quit()

# open new data file for writing
print("[BUILD_MAN_ID_File] Attempting to open output file for writing <BLEach_man_id.py>")
try:
    fidOut = open("BLEach_man_id.py", "w")
except Exception as err:
    print("[BUILD_MAD_ID_File - FATAL] ", str(err))
    print("[BUILD_MAD_ID_File - FATAL] Open error on output file, make sure you have write permissions on the existing folder")
    fidIn.close()
    quit()

# let's track how many ID we convert
numIDs = 0

# pre-pend the template header file
print("[BUILD_MAN_ID_File] Attempting to pre-pend header file to <BLEach_man_id.py>")
try:
    fidHead = open("man_id_template.py", "r")
    header_data = fidHead.read()
except Exception as err:
    print("[BUILD_MAD_ID_File - FATAL] ", str(err))
    print("[BUILD_MAD_ID_File - FATAL] Open/Read error on header file, make sure <man_id_template.py> exists in the current folder")
    quit()

try:
    fidOut.write(header_data)
    fidHead.close()
except Exception as err:
    print("[BUILD_MAD_ID_File - FATAL] ", str(err))
    print("[BUILD_MAD_ID_File - FATAL] Write/Close error on output file")
    fidOut.close()
    fidHead.close()
    fidIn.close()
    quit()

# add timestamp for new file
fidOut.write("#\n# File Last Updated : " + time.asctime(time.localtime()) + "\n#\n")

# add the structure open text
fidOut.write("MANUFACTURERS = {\n")

# read each line
# - input format
#     12345    0x00ab    Text of the Manufacturer Name
#     23456    0x00de    More Text
#
# - output format
#   0x00ab:    "Text of the Manufacturer Name",
#
#
keepReading = True
maxID = 0
while keepReading:
    try:
        oneLine = fidIn.readline()
        # check for end of file
        if( len(oneLine) == 0 ):
            keepReading = False
        else:
            # parse the three values
            vals = oneLine.split()
            # decode the ID code and check if it is higher than we have seen
            int_val = int(vals[0])
            if( int_val > maxID ):
                maxID = int_val
            # re-concatenate the Manufacturer name
            outStr = ""
            for x in range(2,len(vals)):
                outStr += vals[x].replace("\"", "..") + " "
            fidOut.write("    " + vals[1] + ":\t\"" + outStr + "\",\n")
            numIDs += 1
    except Exception as err:
        print("[BUILD_MAD_ID_File - FATAL] ", str(err))
        print("[BUILD_MAD_ID_File - FATAL] Write error on output file")
        # guess we are done
        keepReading = False

# write the structure closing tags
fidOut.write("    0xffff:\t\"<!!SHOULD NOT BE USED!!>\"\n}")
fidOut.write("\nMAN_MAX_ID = " + str(maxID) + "\n")

# close the output file
fidOut.close()

# close the input file
fidIn.close()

# tell the user we are done
print("[BUILD_MAN_ID_File] Grabbed (", numIDs, ") Manufacturer records")
print("[BUILD_MAN_ID_File] Completed Successfully")