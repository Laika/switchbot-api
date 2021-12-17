import json
import os
import time

import schedule
from bluepy.btle import DefaultDelegate, Scanner

macaddr = os.getenv("MAC_ADDR", "FF:FF:FF:FF:FF:FF").lower()
service_uuid = "cba20d00-224d-11e6-9fb8-0002a5d5c51b"
char_uuid = "cba20002-224d-11e6-9fb8-0002a5d5c51b"


class ScanDelegate(DefaultDelegate):
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
        with open("/data/sensor.json", "w") as f:
            sensor_value = {
                "mac": self.macaddr,
                "sensor_type": "SwitchBot",
                "temperature": temp,
                "humidity": humid,
                "battery": batt,
            }
            json.dump(sensor_value, f)


def scan():
    scanner = Scanner().withDelegate(ScanDelegate(macaddr))
    scanner.scan(5.0)


schedule.every(10).seconds.do(scan)

while True:
    schedule.run_pending()
    time.sleep(1)
