import json
import os
import time

import schedule
from bluepy.btle import DefaultDelegate, Scanner

thermometer_macaddr = os.getenv("MAC_ADDR", "FF:FF:FF:FF:FF:FF").lower()
human_detector_macaddr = os.getenv("HUMAN_DETECTOR_MAC_ADDR", "FF:FF:FF:FF:FF:FF").lower()

period = int(os.getenv("PERIOD", "10"))
service_uuid = "cba20d00-224d-11e6-9fb8-0002a5d5c51b"
char_uuid = "cba20002-224d-11e6-9fb8-0002a5d5c51b"


class ThermometerScanDelegate(DefaultDelegate):
    def __init__(self, macaddr):
        DefaultDelegate.__init__(self)
        self.sensorValue = None
        self.macaddr = macaddr

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr != self.macaddr:
            return
        for adtype, desc, value in dev.getScanData():
            if desc == "16b Service Data":
                self._decodeSensorData(value)

    def _decodeSensorData(self, valueStr):
        global sensor_value
        valueBinary = bytes.fromhex(valueStr[4:])
        batt = valueBinary[2] & 0b01111111
        isTemperatureAboveFreezing = valueBinary[4] & 0b10000000
        temp = (valueBinary[3] & 0b00001111) / 10 + (valueBinary[4] & 0b01111111)
        if not isTemperatureAboveFreezing:
            temp = -temp
        humid = valueBinary[5] & 0b01111111
        with open("/data/thermometer.json", "w") as f:
            sensor_value = {
                "mac": self.macaddr,
                "sensor_type": "SwitchBot",
                "temperature": temp,
                "humidity": humid,
                "battery": batt,
            }
            json.dump(sensor_value, f)


class HumanDetectorScanDelegate(DefaultDelegate):
    def __init__(self, macaddr):
        DefaultDelegate.__init__(self)
        self.sensorValue = None
        self.macaddr = macaddr

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr != self.macaddr:
            return
        for adtype, desc, value in dev.getScanData():
            if desc == "16b Service Data":
                if adtype == 22:
                    self._decodeSensorData(value)

    def _decodeSensorData(self, valueStr):
        global sensor_value
        valueBinary = bytes.fromhex(valueStr[4:])
        isON = (valueBinary[1] & 0b01000000) >> 6
        time = valueBinary[4]
        isIlluminance = (valueBinary[5] & 0b00000011) - 1

        with open("/data/human-detector.json", "w") as f:
            sensor_value = {"mac": self.macaddr, "sensor_type": "SwitchBot", "isIllminance": isIlluminance, "isOn": isON, "time": time}
            print(sensor_value)
            json.dump(sensor_value, f)


def scan():
    Scanner().withDelegate(HumanDetectorScanDelegate(human_detector_macaddr)).scan(5.0)
    Scanner().withDelegate(ThermometerScanDelegate(thermometer_macaddr)).scan(5.0)


schedule.every(period).seconds.do(scan)

while True:
    schedule.run_pending()
    time.sleep(1)
