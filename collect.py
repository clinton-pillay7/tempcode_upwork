import json
import os


def parse():
    drives = ["W", 'X', 'Y', 'Z', 'F']
    consolidated = {}
    for drive in drives:
        drvpath = f"{drive}:\\"
        if os.path.exists(drvpath):
            with open(f"{drive}:\\latest_config_measurements.json", 'r') as h:
                datas = json.load(h)
                for data in datas["measurements"]:
                    tempresult = drive,":",data
                    consolidated[drive] = {}
                    consolidated[drive].update(data)
        else:
            consolidated[drive] = {}
            nodriveobj = {'co2_ppm': '-', 
                            'humidity_RH': '-', 
                            'pm01_ugm3': '-', 
                            'pm10_ugm3': '-', 
                            'pm25_AQICN': '-', 
                            'pm25_AQIUS': '-', 
                            'pm25_ugm3': '-', 
                            'temperature_C': '-', 
                            'temperature_F': '-', 
                            'voc_ppb': '-'}
            consolidated[drive].update(nodriveobj)
    return consolidated    
