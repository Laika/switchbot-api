import json

from fastapi import FastAPI

app = FastAPI()


@app.get("/api/thermometer")
async def all():
    try:
        with open("/data/thermometer.json") as f:
            sensor = json.load(f)
    except Exception:
        sensor = {
            "mac": None,
            "sensor_type": "SwitchBot",
            "temperature": None,
            "humidity": None,
            "battery": None,
        }
    return sensor


@app.get("/api/human-detector")
async def all():
    try:
        with open("/data/human-detector.json") as f:
            sensor = json.load(f)
    except Exception:
        sensor = {
            "mac": None,
            "sensor_type": "SwitchBot",
            "temperature": None,
            "humidity": None,
            "battery": None,
        }
    return sensor
