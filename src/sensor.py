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
        super().__init__()
        self.sensorValue = None
        self.macaddr = macaddr

    def handleDiscovery(self, dev, is_new_dev, is_new_data):
        if dev.addr != self.macaddr:
            return
        for adtype, desc, value in dev.getScanData():
            if desc == "16b Service Data":
                self._decodeSensorData(value)

    def _decodeSensorData(self, value: str):
        value = bytes.fromhex(value[4:])
        batt = value[2] & 0b01111111
        isTemperatureAboveFreezing = value[4] & 0b10000000
        temp = (value[3] & 0b00001111) / 10 + (value[4] & 0b01111111)
        if not is_temperature_above_freezing:
            temp = -temp
        humid = value[5] & 0b01111111

        self.sensor_value = {
            "mac": self.macaddr,
            "sensor_type": "SwitchBot",
            "temperature": temp,
            "humidity": humid,
            "battery": batt,
        }


class HumanDetectorScanDelegate(DefaultDelegate):
    def __init__(self, macaddr):
        super().__init__()
        self.sensor_value = None
        self.macaddr = macaddr

    def handleDiscovery(self, dev, is_new_dev, is_new_data):
        if dev.addr != self.macaddr:
            return
        for adtype, desc, value in dev.getScanData():
            if adtype == 22 and desc == "16b Service Data":
                self._decodeSensorData(value)

    def _decodeSensorData(self, value: str):
        value = bytes.fromhex(value[4:])
        is_on = (valueBinary[1] & 0b01000000) >> 6
        time = valueBinary[4]
        is_illuminance = (valueBinary[5] & 0b00000011) - 1

        self.sensor_value = {
            "mac": self.macaddr,
            "sensor_type": "SwitchBot",
            "isIlluminance": is_illuminance,
            "isOn": is_on,
            "time": time,
        }
