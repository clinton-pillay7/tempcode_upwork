import json
import os


drives = ['W:', 'X:', 'Y:', 'Z:', "F:"]


def checkdrv(drives):
    drives = ['W:', 'X:', 'Y:', 'Z:', "F:"]

    drive_status = []

    for drive in drives:
        status = "reachable" if os.path.exists(drive) else "not reachable"
        drive_status.append({"drive": drive, "status": status})

    return drive_status 

def parse():
    with open('X:\\latest_config_measurements.json', 'r') as f:
        data = json.load(f)
    
    measurements = data["measurements"]
    co2_ppm = measurements[0]['co2_ppm']
    humidity_RH = measurements[0]['humidity_RH']
    pm01_ugm3 = measurements[0]['pm01_ugm3']
    pm10_ugm3 = measurements[0]['pm10_ugm3']
    pm25_AQICN = measurements[0]['pm25_AQICN']
    pm25_AQIUS = measurements[0]['pm25_AQIUS']
    pm25_ugm3 = measurements[0]['pm25_ugm3']
    temperature_C = measurements[0]['temperature_C']
    temperature_F = measurements[0]['temperature_F']
    voc_ppb = measurements[0]['voc_ppb']

    return co2_ppm, humidity_RH, pm01_ugm3, pm10_ugm3, pm25_AQICN, pm25_AQIUS, pm25_ugm3, temperature_C, temperature_F, voc_ppb


result  = parse()
print(result)
