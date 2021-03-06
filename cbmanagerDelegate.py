import time
from PyObjCTools import AppHelper
from bleachDevice import bleDevice

class managerDelegate(object):

    def __init__(self):
        print("[BLEDelegate INFO] instantiated")
        self.DELTATIME = 0
        self.STARTTIME = time.time()
        self.devices = list(())
        self.isConnectable = False
        self.debug = False

    def setTimeout(self, secs):
        self.RUNTIME = secs

    def setParams(self, onlyConnectable=False, debugFlag=True ):
        # set the processing flags
        # isConnectable - onlhy grab devices that are connectable
        self.isConnectable = onlyConnectable
        self.debug = debugFlag

    def getDevices(self):
        return self.devices

    def centralManagerDidUpdateState_(self, manager):
        print("[BLEDelegate INFO] Scanning")
        self.manager = manager
        manager.scanForPeripheralsWithServices_options_(None,None)

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self, manager, peripheral, data, rssi):
        self.peripheral = peripheral
        self.data = data
        localName = "<NotSet>"

        if( peripheral is not None ):
            # only do this if the return value is valid
            newDevice = bleDevice()
            # grab the device information
            newDevice.setPeripheral(peripheral)
            newDevice.setAddress(peripheral.identifier())
            newDevice.setRSSI( rssi )
            
            # grab the manufacturers data
            if( data is not None ):
                newDevice.setData(data)
                # check if we can grab a local name
                localName = data.get("kCBAdvDataLocalName", "<NoName>")
                # grab the data channel if it is present
                dataChannel = data.get("kCBAdvDataChannel", 0)
                newDevice.setChannel(dataChannel)
                # grab connectable flag
                canConnect = data.get("kCBAdvDataIsConnectable", 0)
                if( canConnect == 1):
                    newDevice.setConnectable(True)
                # see if there are any service UUIDs advertized
                uuidList = data.get("kCBAdvDataServiceUUIDs", None )
                if( uuidList is not None ):
                    newDevice.setServiceIDs(uuidList)
                # check if TX power is available kCBAdvDataTxPowerLevel
                pwr = data.get("kCBAdvDataTxPowerLevel", 0 )
                newDevice.setTxPower(pwr)
                # check for special "Apple" data
                appleData = data.get("kCBAdvDataAppleMfgData", None )
                if( appleData is not None):
                    newDevice.setAppleData(appleData)
                    # grab the data from the advanced data dictionary
                    advAppleData = appleData.get("kCBScanOptionAppleFilterPuckType", -1)
                    newDevice.setApplePuckType(advAppleData)
                # check for advanced manufacturing data
                moreData = data.get("kCBAdvDataManufacturerData", None )
                if( moreData is not None ):
                    newDevice.setAdvData(moreData)

            # check if they found a name
            if( peripheral.name() is not None ):
                newDevice.setName( str(peripheral.name()) )
            else:
                newDevice.setName( localName )
            
            if( self.isConnectable == True ):
                # only save this device if it is connectable
                if( newDevice.isConnectable() == True ):
                    print("[BLEDelegate FOUND - Connectable] ", newDevice.getName(), " , ", newDevice.getAddress() )
                    self.devices.append(newDevice)
                else:
                    print("[BLEDelegate IGNORED - NotConnectable] ", newDevice.getName(), " , ", newDevice.getAddress() )
            else:
                # save regardless of connection state
                print("[BLEDelegate FOUND] ", newDevice.getName(), " , ", newDevice.getAddress() )
                self.devices.append(newDevice)
        
        else:
            print( "[BLEDelegate ERROR] null peripheral returned in didDiscover)" )

        
        # check elapsed time and stop the scan
        self.DELTATIME = time.time() - self.STARTTIME
        if( self.DELTATIME > self.RUNTIME ):
            manager.stopScan()
            AppHelper.stopEventLoop()
        
        # sample connect if found
        # if '9B4D5446-C91D-4DCA-9D68-F70A2CB3FF71' in repr(self.peripheral.UUID):
        if 'FB40F718-6C78-4695-B671-8BDD896E8810' in repr(self.peripheral.UUID):
            try:
                print( 'DeviceName ' + localName)
                manager.connectPeripheral_options_(self.peripheral, None)
                manager.stopScan()
            except Exception as err:
                print( "[BLEDelegate FATAL] Exception (", str(err), ") trying to connect to peripheral")

    def centralManager_didConnectPeripheral_(self, manager, peripheral):
        print("in didConnect")
        print( repr(peripheral.UUID()) )
        self.peripheral.setDelegate_(self)
        self.peripheral.discoverServices_(None)

    def peripheral_didDiscoverServices_(self, peripheral, services):
        print("in didDiscoverServ\n")
        self.service = self.peripheral.services()[0]
        print( self.peripheral.services() )
        self.peripheral.discoverCharacteristics_forService_(None, self.service)

    def peripheral_didDiscoverCharacteristicsForService_error_(self, peripheral, service, error):
        print("in didDiscoverChar")

        for characteristic in self.service.characteristics():
            print(characteristic)
            if characteristic.properties() == 18:
                peripheral.readValueForCharacteristic_(characteristic)
                break
        
        AppHelper.stopEventLoop()

    def peripheral_didWriteValueForCharacteristic_error_(self, peripheral, characteristic, error):
        print( 'In error handler' )
        print( 'ERROR:' + repr(error) )

    def peripheral_didUpdateNotificationStateForCharacteristic_error_(self, peripheral, characteristic, error):
        print( "Notification handler" )

    def peripheral_didUpdateValueForCharacteristic_error_(self, peripheral, characteristic, error):
        print("in didUpdateValue")
        print( repr(characteristic.value().bytes().tobytes()) )
        value = characteristic.value().bytes().tobytes()