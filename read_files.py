import os
import cv2
import pytesseract
from PIL import Image
from pytesseract import pytesseract
from PIL import Image
from moviepy.editor import *
import os
from   datetime        import datetime, timedelta

# Importing all necessary libraries



# Download video for processing from ptth
import requests
import shutil
import json
import sys
from   lxml            import html
from   time            import sleep
from   shutil          import copyfileobj, move
from   datetime        import datetime, timedelta
from moviepy.editor import *
#10093015 2023-06-13 22:26:29-0500, Response, 1686713189229, 1168671337, curl return: 0, https return: 200, {"RequestId":"cef84462-2888-483c-80bb-51f673e1ef0f","TotalSeconds":1.0508878,"FROM":"02763288f5be6962b"}, 44.240.206.169
#sensor_number='10100002'
#date="2023:06:15"
#date=date.replace(":","_")
#time="13:39:05"
#time=time.replace(":","-")
#beforetime=alert_log_line['timestamp'][11:19]
#beforetime=beforetime.replace(":","-")
#timestamp='1229780677'
#date_time=date+"_"+time
date = sys.argv[1]
time = sys.argv[2]
date_time=sys.argv[3]
timestamp=sys.argv[4]
sensor_number=sys.argv[5]
date_time=sensor_number+"_"+date_time



folder_paths = ['./Desktop/video_download_project/collected_frames', './Desktop/video_download_project/data', './Desktop/video_download_project/Video_input']

for folder_path in folder_paths:
    # Get list of all files in folder
    file_list = os.listdir(folder_path)

    # Loop through files and delete each one
    for filename in file_list:
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)
        
videos_dir_valpath=r'.\Desktop\video_download_project\Video_input'
if not os.path.exists(videos_dir_valpath):
    os.makedirs(videos_dir_valpath)
def getSiteData(sitesURL, siteHeaders):
    print("Getting site data...")
    
    payload     = {}
    response    = requests.request("GET", sitesURL, headers = siteHeaders, data = payload)

    data        = json.loads(response.text)['sites']
    print(data)
    return data
siteHeaders         = {
        'X-ApiKey': 'a832bf3d-26af-4397-a750-bf718369dee0'
    }
serverHeaders       = {
        'X-ApiKey': 'bony lend plaza used crave clink nap blush patio talon'
    }
sitesURL = r"https://data.vstalert.com/Sync/GetAllBranchesAndSensors"
baseURL             = F"https://vstalert-update.com/ptth/scraper/v1"
serversURL          = F"{baseURL}/server_list"
siteData    = getSiteData(sitesURL, siteHeaders)


# Sends a request to retrieve server data.
# Returns a list of server names which contain the substring defined in the "server" variable.

# getSiteData(sitesURL,siteHeaders)
def getServerLogs(baseURL,serverHeaders,sensor_number,dateBegin,time):
        url = F"{baseURL}/server/{sensor_number}/files/VST_SD/DashVideos/"
        response = requests.request('GET', url, headers = serverHeaders)
        tree           = html.fromstring(response.content)
        allLinks       = tree.xpath('//a[@class="entry"]/@href')
        print(allLinks)
        picNames     =  [
                            
                            (url, link) for link in allLinks if
                                link.endswith('.avi') and 
                                datetime.strptime(link[2:12], "%Y_%m_%d") == datetime.strptime(dateBegin,  "%Y_%m_%d") and
                              ( datetime.strptime(time,"%H-%M-%S")>= (datetime.strptime(link[13:21],"%H-%M-%S")))]
        #print(picNames)
        return picNames
        
        # print(allLinks)
def downloadServerLogs( name,serverHeaders):
    
    logData = [None,None]
    while(not logData[1] or logData[1].status_code != 200):
        try:
            logData = (name, requests.get(''.join(name), stream = True, headers = serverHeaders))
        except (ConnectionError,TimeoutError,requests.exceptions.ConnectionError) as e:
            print(F"ERROR:  {e}\n  {type(e)} in:  {''.join(name)}")
            sleep(3)
    # print(requests.get(''.join(name), stream = True, headers = serverHeaders).content)
    logData[1].raw.decode_content = True
    with open(F"./Desktop/video_download_project/Video_input/{logData[0][1][2:21]}.avi", 'wb') as f:
           shutil.copyfileobj(logData[1].raw, f)
           
def getServerLogs1(baseURL,serverHeaders,sensor_number,dateBegin,time):
        url = F"{baseURL}/server/{sensor_number}/files/VST_SD/DashVideos/"
        response = requests.request('GET', url, headers = serverHeaders)
        tree           = html.fromstring(response.content)
        allLinks       = tree.xpath('//a[@class="entry"]/@href')
        print(allLinks)
        picNames     =  [
                            
                            (url, link) for link in allLinks if
                                link.endswith('.avi') and 
                                datetime.strptime(link[2:12], "%Y_%m_%d") == datetime.strptime(dateBegin,  "%Y_%m_%d") and
                              ( datetime.strptime(time,"%H-%M-%S")< (datetime.strptime(link[13:21],"%H-%M-%S")))]
        #print(picNames)
        return picNames
    

output=getServerLogs(baseURL,serverHeaders,sensor_number,date,time)
downloadServerLogs(output[-1],serverHeaders)


present_video_info=getServerLogs(baseURL,serverHeaders,sensor_number,date,time)
next_video_info=getServerLogs1(baseURL,serverHeaders,sensor_number,date,time)
print(present_video_info[-1])
print(next_video_info[0])
tuple3,tuple4=(next_video_info[0])
tuple1,tuple2=(present_video_info[-1])
start_time_of_video=tuple2[13:21]
#start_time_of_video_astra=tuple2[11:19]
start_time_of_video=start_time_of_video.replace("-",":")
#start_time_of_video=start_time_of_video_astra.replace("-",":")
next_video_start_time_of_video=tuple4[13:21]
#next_video_start_time_of_video_astra=tuple4[11:19]
next_video_start_time_of_video=next_video_start_time_of_video.replace("-",":")
#next_video_start_time_of_video=next_video_start_time_of_video_astra.replace("-",":")
time=time.replace("-",":")
time_format = '%H:%M:%S'
#last_video_time=last_video_time.replace("-",":")
start_time_of_video = datetime.strptime(start_time_of_video, time_format)
next_video_start_time_of_video = datetime.strptime(next_video_start_time_of_video, time_format)
print(start_time_of_video)
print(next_video_start_time_of_video)
diff= (next_video_start_time_of_video-start_time_of_video).total_seconds()
print(diff)

alert_time=datetime.strptime(time, time_format)

from moviepy.editor import VideoFileClip
import os

def get_video_duration(file_path):
    video = VideoFileClip(file_path)
    duration = video.duration
    return duration

# Example usage
folder_path = r'.\Desktop\video_download_project\Video_input'  # Update with the actual folder path
video_files = [f for f in os.listdir(folder_path) if f.endswith('.avi')]  # Filter for video files (change the extension if necessary)

for video_file in video_files:
    file_path = os.path.join(folder_path, video_file)
    output = get_video_duration(file_path)
proportion_factor=output/diff
print(proportion_factor)

alert_difference_between_video_start_time_and_alert_time=(alert_time-start_time_of_video).total_seconds()
print(alert_difference_between_video_start_time_and_alert_time)
time_used_to_clip=alert_difference_between_video_start_time_and_alert_time*proportion_factor
print(alert_difference_between_video_start_time_and_alert_time*proportion_factor)


#Determine the start time of the video to be clipped based on time of alert and start time of the video
if time_used_to_clip-200<0:
    if time_used_to_clip-150<0:
        if time_used_to_clip-100<0:
            if time_used_to_clip-50<0:
                if time_used_to_clip-40<0:
                    if time_used_to_clip-30<0:
                        if time_used_to_clip-20<0:
                            if time_used_to_clip-10<0:
                                start_time_of_video=time_used_to_clip
                            else:
                                start_time_of_video=time_used_to_clip-10
                        else:
                            start_time_of_video=time_used_to_clip-20
                else:
                    start_time_of_video=time_used_to_clip-40
            else:
                start_time_of_video=time_used_to_clip-50
        else:
            start_time_of_video=time_used_to_clip-100
    else:
        start_time_of_video=time_used_to_clip-150
else:
    start_time_of_video=time_used_to_clip-200
        
#clipping the video
video_name=(os.listdir("./desktop/video_download_project/video_input"))[0]
clip = VideoFileClip("./desktop/video_download_project/video_input/"+(video_name))
clip =clip.subclip(start_time_of_video,time_used_to_clip+200)
clip.write_videofile("./Desktop/video_download_project/clip_video_input/clip.avi",codec='libx264')
#Parse videos present in the folder

folder_path = './Desktop/video_download_project/clip_video_input'  # Replace with the actual path to the folder


video_extensions = ('.mp4', '.avi', '.mkv')  # Add any other video extensions you want to include

video_paths = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(video_extensions):
            video_path=(os.path.join(root, file))
            video_paths.append(video_path.replace('\\', '/'))

#convert video to frames
# Read the video from specified path
cam = cv2.VideoCapture(video_paths[0])
#print(cam.read())
try:
	# creating a folder named data
	if not os.path.exists('./Desktop/video_download_project/data'):
		os.makedirs('./Desktop/video_download_project/data')

# if not created then raise error
except OSError:
	print ('Error: Creating directory of data')

# frame
currentframe = 0
print(cam)
print(cam.read())
while(True):
	
	# reading from frame
	ret,frame = cam.read()

	if ret:
		# if video is still left continue creating images
		name = './Desktop/video_download_project/data/frame' + str(currentframe) + '.jpg'
		print ('Creating...' + name)

		# writing the extracted images
		cv2.imwrite(name, frame)

		# increasing counter so that it will
		# show how many frames are created
		currentframe += 1
	else:
		break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()



folder_path = './Desktop/video_download_project/data'
files=os.listdir("./Desktop/video_download_project/data")
file_list=[]
for filename in files:
    file_list.append(filename)
monotonic_ms=timestamp

import re
# Define a regular expression pattern to extract the frame number
pattern = re.compile(r'frame(\d+)\.jpg')
# Define a function to extract the frame number from a filename
def extract_frame_number(filename):
    match = pattern.search(filename)
    return int(match.group(1))
# Sort the list of filenames based on their frame number
sorted_filenames = sorted(file_list, key=extract_frame_number)

#print(sorted_filenames)
path_to_tesseract = r'C:\Users\User\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
count=0
i=0
extracted_Frame_no=None
pytesseract.tesseract_cmd = path_to_tesseract

while i <=((len(sorted_filenames))):
    print(i)
    y=0
    path_to_image=(os.path.join("./Desktop/video_download_project/data", sorted_filenames[i]))
    image = Image.open(path_to_image)

# Define the pixel range to extract
    left = 37
    upper = 180
    right = 116
    lower = 195

# Crop the image to the specified range
    crop_image = image.crop((left, upper, right, lower))

#Extract text from image
    text = pytesseract.image_to_string(crop_image)

    print((text))
    count+=1
    
    #if monotonic_ms>=str(int(monotonic_ms)-100) and monotonic_ms<=str(int(monotonic_ms)+100) in text:
        #print(f"Reference image is present in {sorted_filenames[i]}")
        #print("yes")
        #break
    print(type(monotonic_ms))
    lower_bound = int(monotonic_ms[0:8])-1
    upper_bound = int(monotonic_ms[0:8])-1
    
    lower_bound1=int(monotonic_ms[0:7])-1
    upper_bound1=int(monotonic_ms[0:7])+1

# Define the regular expression pattern to search for
    pattern = re.compile(r"\b(" + "|".join(str(i) for i in range(lower_bound, upper_bound + 1)) + r")\b")
    
    pattern1 = re.compile(r"\b(" + "|".join(str(i) for i in range(lower_bound1, upper_bound1 + 1)) + r")\b")

# Search for the pattern in the text
    matches = re.findall(pattern, text[0:8])
    matches1 = re.findall(pattern1, text[0:7])
# Print out any matches found
    if matches:
        print("Found the following matches:", ", ".join(matches))
        print(sorted_filenames[i])
        extracted_Frame_no=sorted_filenames[i]
        break
    elif matches1:
        print("Found the following matches:", ", ".join(matches1))
        print(sorted_filenames[i])
        extracted_Frame_no=sorted_filenames[i]
        break
    else:
        print("No matches found")
    
    #if  monotonic_ms[0:7].isdigit():
        #if (int(monotonic_ms[0:7])+10000)<int(text[0:7]):
            #print("No matches found")
    for j in range(7,0,-1):
        #print(j)
        if str(int(monotonic_ms[0:2])-j) in text[0:2]:
                y=50
                break
        elif  str(int(monotonic_ms[0:3])-j)  in text[0:3]:
                y=50
                break
        elif str(int(monotonic_ms[0:4])-j) in text[0:4]:
                y=20
                break
        elif str(int(monotonic_ms[0:5])-j) in text[0:5]:
                y=5
                break
    if y==50:
        i+=50
    elif y==20:
        i+=20
    elif y==5:
        i+=5
    else:
        i+=2
        
# Set the number of frames to extract before and after the specified frame
num_frames_before = 100
num_frames_after = 50



# Create a new folder to save the extracted frames
new_folder_path = './Desktop/video_download_project/collected_frames'

if extracted_Frame_no is not None:
    # Get the index of the first digit in the filename
    first_digit_index = next((i for i, c in enumerate(extracted_Frame_no) if c.isdigit()), None)

    # Get the index of the last digit in the filename
    last_digit_index = max([i for i, c in enumerate(extracted_Frame_no) if c.isdigit()])

    # Extract the frame number from the filename
    frame_num = int(extracted_Frame_no[first_digit_index:last_digit_index+1])

    # Iterate through the frames in the folder
    for i, filename in enumerate(sorted_filenames):
    #print(i, filename)
    # Check if the file is a valid image file
        if filename.endswith('.jpg') or filename.endswith('.png'):
        # Read the frame
            frame = cv2.imread(os.path.join(folder_path, filename))
        
        # Check if the current frame number is within the range of frames to extract
            if i >= frame_num - num_frames_before and i <= frame_num + num_frames_after:
            # Save the frame to the new folder
                new_filename = f'{i}.jpg'
                cv2.imwrite(os.path.join(new_folder_path, new_filename), frame)
    
        
    
print(count)
print(len(files))
#print(files[0])

from os.path import isfile, join
import numpy as np
def convert_frames_to_video(pathIn,pathOut,fps):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
    # #for sorting the file names properly
    #files.sort(key = lambda x: int(x[5:-4]))
    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        print(filename)
        #inserting the frames into an image array
        frame_array.append(img)

    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()

def main():
    pathIn= './Desktop/video_download_project/collected_frames/'
    pathOut = './Desktop/video_download_project/reframed-video/{}.avi'.format(date_time)
    fps = 10

    folder_path = "./Desktop/video_download_project/collected_frames" # replace with your folder path

    # get all files in folder
    files = os.listdir(folder_path)

    if len(files) == 0:
         print("The folder is empty.Couldn't find the monotonic timestamp")
    else:
        (convert_frames_to_video(pathIn, pathOut, fps))

if __name__=="__main__":
    main()



#delete all files in folders

folder_paths = ['./Desktop/video_download_project/collected_frames', './Desktop/video_download_project/data', './Desktop/video_download_project/Video_input']

for folder_path in folder_paths:
    # Get list of all files in folder
    file_list = os.listdir(folder_path)

    # Loop through files and delete each one
    for filename in file_list:
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)