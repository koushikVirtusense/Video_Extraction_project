import json
import subprocess
with open('./Desktop/video_download_project/data/loaded_data/curlLog_input/alertlogs_sent_to_cloud.txt','r') as f1:
                    for line in f1:
                        splitted_line=line.split(",")
                        sensor_number=line[0:8]
                        date = line[9:19]
                        date=date.replace("-","_")
                        time = line[20:28]
                        time=time.replace(":","-")
                        date_time=date+"_"+time
                        timestamp=splitted_line[3].strip()
                        print(sensor_number+"_"+date+"_"+time+"_"+timestamp)
                        subprocess.run(['python', './Desktop/video_download_project/read_files.py', date, time,date_time,timestamp,sensor_number],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
