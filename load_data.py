import os
import shutil
from pathlib import Path

# function to filter the site and datetime of source data
def loadTimeRangeList(year, month, start_date, end_date):
    res = list()
    year_month = '_'.join([year, month])
    for date in range(start_date, end_date + 1):
        date = '0' + str(date) if len(str(date)) == 1 else str(date)
        res.append('_'.join([year_month, date]))
    return res

# current data time range [07/26, 09/13] (include)
time_list = loadTimeRangeList('2023', '06', 19, 25) 
print("loading data from following dates: ", time_list)

# (10052001, 10052013), (10033001, 10033029), (10004051, 10004064)
sensor_range = [(10083026,10083046)]
# sensor_range = [(10052001, 10052013), (10047001, 10047016), (10045001, 10045022), (10043001, 10043030), \
#     (10042001, 10042035), (10041001, 10041028), (10036001, 10036047), (10033001, 10033029), (10032002, 10032039), \
#     (10031001, 10031037), (10015003, 10015051), (10004051, 10004064)]
print("loading data from following sensor range: ", sensor_range)
sensor_list = list()
for i, j in sensor_range:
    for s in range(i, j + 1):
        sensor_list.append(str(s))


curlLog_dir_path = r'.\Desktop\video_download_project\data\loaded_data\curlLog_input'


# Read all the input txt files to a new folder

if not os.path.exists(curlLog_dir_path):
    os.makedirs(curlLog_dir_path)
directory = r'.\data\raw_data'
for subdir in os.listdir(directory):
    subdir = os.path.join(directory, subdir)
    if os.path.isdir(subdir):
        for sensor in os.listdir(subdir):
            sensor = os.path.join(subdir, sensor)
            for filename in os.listdir(sensor):
                cur_info_list = filename.split('-')[0]
                cur_info_list = cur_info_list.split('_')
                cur_sensor = cur_info_list[0]
                cur_time = '_'.join(cur_info_list[1:])
                #if filename.endswith(".avi"):
                #    input = os.path.join(sensor, filename)
                #    if cur_sensor in sensor_list and cur_time in time_list:
                #        shutil.copy2(input, videos_dir_valpath)
                if filename.endswith(".txt"):
                    # print(cur_sensor, cur_time)
                    # redirect alertLog files
                    # if 'alertLog' in filename:
                    input = os.path.join(sensor, filename)
                    if cur_sensor in sensor_list and cur_time in time_list:
                        shutil.copy2(input, curlLog_dir_path)
                    # redirect curlLog files
                #     if 'curlLog' in filename:
                #         input = os.path.join(sensor, filename)
                #         if cur_sensor in sensor_list and cur_time in time_list:
                #             shutil.copy2(input, curlLog_dir_path)
                if filename.endswith(".png"):
                       #redirect raw snapshot files
                    #if '_Bed' in filename:
                    input = os.path.join(sensor, filename)
                    if cur_sensor in sensor_list and cur_time in time_list:
                        shutil.copy2(input, rawPic_dir_testpath)