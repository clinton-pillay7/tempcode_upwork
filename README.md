This aims to satisfy the below problem:  


Summary
I am currently running Python v3.10 on Windows PC.

I have sound-Quality Monitor device (4 quantity) on LAN which I can access via network mapped folder to get its current stats file.

I need a python script which will:

1) access network mapped drive 'W'
2) open file latest_config_measurements.json (sample attached)
3) extract values for:
        "timestamp"
        "db"
        "db_RH"
        "pm01_ugm3"
        "pm10_ugm3"
        "pm25_ugm3"
        "temperature_C"
        "voc_ppb"
4) repeat step 1-3 for network mapped drive 'X', 'Y', 'Z'
5) create html email:
from: x@x.x
to: y@y.y
subject: soundQuality
body: table (sample attached)
Column A: fixed
Office: row values from drive W
Bedroom: row values from drive X
Kitchen: row values from drive Y
Outdoor: row values from drive Z
* if drive is not accessible then insert "-" in column B-I
Column B: convert "timestamp" value to dd/mm/yy hh:mm; insert dd/mm/yy hh:mm
Column C: insert value of "pm01_ugm3"; color cell as per range in AQ-Range.xls
Column D: insert value of "pm25_ugm3"; color cell as per range in AQ-Range.xls
Column E: insert value of "pm10_ugm3"; color cell as per range in AQ-Range.xls
Column F: insert value of "voc_ppb"; color cell as per range in AQ-Range.xls
Column G: insert value of "db"; color cell as per range in AQ-Range.xls
Column H: insert value of "db_RH"; color cell as per range in AQ-Range.xls
Column I: insert value of "temperature_C"; color cell as per range in AQ-Range.xls
6) send email
7) exit script
