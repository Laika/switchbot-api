import json
import logging
import os

from bluepy.btle import DefaultDelegate, Scanner
from fastapi import FastAPI

from sensor import HumanDetectorScanDelegate, ThermometerScanDelegate

app = FastAPI()

logger = logging.getLogger(__name__)

thermometer_macaddr: str = os.getenv("THERMOMETER_MAC_ADDR", "FF:FF:FF:FF:FF:FF").lower()
human_detector_macaddr: str = os.getenv("HUMAN_DETECTOR_MAC_ADDR", "FF:FF:FF:FF:FF:FF").lower()

period: int = int(os.getenv("PERIOD", "10"))
timeout: float = float(os.getenv("TIMEOUT", "5.0"))
SERVICE_UUID = "cba20d00-224d-11e6-9fb8-0002a5d5c51b"
CHAR_UUID = "cba20002-224d-11e6-9fb8-0002a5d5c51b"

logger.info(f"MAC_ADDR: {thermometer_macaddr}")


@app.get("/api/thermometer")
async def thermometer():
    try:
        scanner = Scanner().withDelegate(ThermometerScanDelegate(thermometer_macaddr))
        scanner.scan(timeout)
        value = scanner.delegate.sensor_value
        logger.info(value)
    except Exception as e:
        logger.error(e)
        value = {
            "mac": None,
            "sensor_type": "SwitchBot",
            "temperature": None,
            "humidity": None,
            "battery": None,
        }
    return sensor


@app.get("/api/human-detector")
async def human_detector():
    try:
        scanner = Scanner().withDelegate(HumanDetectorScanDelegate(human_detector_macaddr))
        scanner.scan(timeout)
        value = scanner.delegate.sensor_value
        logger.info(value)
    except Exception as e:
        logger.error(e)
        value = {
            "mac": None,
            "sensor_type": "SwitchBot",
            "temperature": None,
            "humidity": None,
            "battery": None,
        }
    return sensor
