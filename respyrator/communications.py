
class CommunicationFrame:
    def __init__(self, dataStream):
        numberOfAddresses = len(self.getAddress())
        expectedBits = numberOfAddresses*4
        self._dataFrame = [ None ] * numberOfAddresses
        if dataStream > pow(2,expectedBits)-1:
            raise ValueError("RX ctor. : Invalid data stream")
        hexRep = '0x{0:0{1}X}'.format(dataStream, numberOfAddresses)
        for n in range(numberOfAddresses):
            self._dataFrame[n] = hexRep[n+2]

    def get(self, address):
        if isinstance(address, str) and self.getAddress():
            addressNum = self.getAddress()[address]
        elif isinstance(address, int) and address < len(self.getAddress()):
            addressNum = address
        else:
            raise ValueError("Invalid address type")
        return int ( self._dataFrame[addressNum] )

class RX(CommunicationFrame): 
    address = {
        "header"                   : 0x00,
        "protocolVersion"          : 0x01,
        "frameNumber"              : 0x02,
        "command"                  : 0x03,
        "valueHB"                  : 0x04, # High byte
        "valueLB"                  : 0x05, # Low byte
        "crc"                      : 0x06
    }
    command = {
        "setRPM"                   : 0x01,
        "setPeakPressure"          : 0x02,
        "setPeepPressure"          : 0x03,
        "setTriggerFlow"           : 0x04,
        "setRamp"                  : 0x05,
        "setAlarmVolumeLow"        : 0x11,
        "setAlarmVolumeHigh"       : 0x12,
        "setAlarmRPMLow"           : 0x13,
        "setAlarmRPMHigh"          : 0x14,
        "setAlarmPeakPressureLow"  : 0x15,
        "setAlarmPeakPressureHigh" : 0x16,
        "setAlarmPeepPressureLow"  : 0x17,
        "setAlarmPeepPressureHigh" : 0x18,
        "setAlarmBatteryLow"       : 0x19,
        "getAlarmVolumeLow"        : 0x21,
        "getAlarmVolumeHigh"       : 0x22,
        "getAlarmRPMLow"           : 0x23,
        "getAlarmRPMHigh"          : 0x24,
        "getAlarmPeakPressureLow"  : 0x25,
        "getAlarmPeakPressureHigh" : 0x26,
        "getAlarmPeepPressureLow"  : 0x27,
        "getAlarmPeepPressureHigh" : 0x28,
        "getAlarmBatteryLow"       : 0x29,
        "getFimwareVersion"        : 0x50
    }

    def __init__(self, dataStream):
        CommunicationFrame.__init__(self, dataStream)
    def getAddress(self):
        return self.address

# class TX(CommunicationFrame):
#     address = {
#         "header"                : 0x00,
#         "protocolVersion"       : 0x01,
#         "uuid"                  : 0x02,
#         "sn"                    : 0x06, # Serial number
#         "settingRPMHB"          : 0x0A,
#         "settingRPMLB"          : 0x0B,
#         "measureRPMHB"          : 0x0C,
#         "measureRPMLB"          : 0x0D,
#         "settingPeakPressureHB" : 0x0E,
#         "settingPeakPressureLB" : 0x0F,
#         "measurePeakPressureHB" : 0x10,
#         "measurePeakPressureLB" : 0x11,
#         "settingPeepPressureHB" : 0x12,
#         "settingPeepPressureLB" : 0x13,
#         "PeepPressure measureHB": 0x14,
#         "PeepPressure measureLB": 0x15,
#         "settingTriggerFlowHB"  : 0x16,
#         "settingTriggerFlowLB"  : 0x17,
#         "measureFlowHB"         : 0x18,
#         "measureFlowLB"         : 0x19,
#         "settingRampHB"         : 0x1A,
#         "settingRampLB"         : 0x1B,
#         "activeAlarmCode"       : 0x1C,
#         "Status Bit Field"      : 0x1D,
#         "tempValueEnc1"         : 0x1E,
#         "tempValueEnc2"         : 0x1F,
#         "tempValueEnc3"         : 0x20,
#         "tempValueEnc4"         : 0x21,
#         "answerHB"              : 0x22,
#         "answerLB"              : 0x23,
#         "answerToFrameNumber"   : 0x24,
#         "crc"                   : 0x25
#     }
