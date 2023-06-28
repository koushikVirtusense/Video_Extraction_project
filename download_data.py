# This script call getLogsFromPtth.py to download logs from sensors in sensor_range

import os

start_date = '2023-06-25'
sensor_list = []

# Removed sensors from range: 10024001 - 10024042 and 10053001 - 10053011

sensor_range = [(10083026,10083046)]

# We want data points only from these sensors: 10036001 - 10036047 Yale 

# sensor_range = [(10036001, 10036047)]

for i, j in sensor_range:
    for s in range(i, j + 1):
        sensor_list.append(s)

sensor_list_str = ' '.join(str(s) for s in sensor_list)
# print(sensor_list_str)

os.system(r"python .\Desktop\video_download_project\getLogsFromPtth.py -f .\data\raw_data -d " + start_date + " -s " + sensor_list_str)
