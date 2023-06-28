import labelbox
from labelbox import Client
import os

##Display projects in labelbox
client = Client(api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjbGZpdG1rZmsxMGc2MDd4dTAzaTU1dXk2Iiwib3JnYW5pemF0aW9uSWQiOiJja2l2enNpMXR5cmNvMDc0MWczbXEwaGtwIiwiYXBpS2V5SWQiOiJjbGlrYWNncGIwYThqMDd3emZzczczOXJrIiwic2VjcmV0IjoiNTU2OWU1OGNmYmFiMTE4OTY1NmFjZTQ2MWEyNmJkZDAiLCJpYXQiOjE2ODYwNTYyMjksImV4cCI6MjMxNzIwODIyOX0.lW7RRRuqGvi6--1hIDf08h62-rKaHT2wBwSElKQgDkw')
projects = client.get_projects()
for project in projects:
    print(project.name)

##See if a particular dataset is present in labelbox,if not create a new dataset in labelbox
# Define the folder path where your videos are stored
VIDEO_FOLDER = './Desktop/video_download_project/new'

# Get a list of video files in the folder
video_files = [f for f in os.listdir(VIDEO_FOLDER) if os.path.isfile(os.path.join(VIDEO_FOLDER, f))]

# Loop through each video file
for video_file in video_files:
    dataset_name=(video_file[0:8])
    # Extract the data name from the video file name (assuming it's before the extension)
    datasets = client.get_datasets(where=labelbox.Dataset.name == dataset_name)
    dataset = next(iter(datasets), None)

    if dataset:
        #dataset = datasets.first()
        file_path = os.path.join(VIDEO_FOLDER, video_file)
        data_row = dataset.create_data_row(row_data=file_path,external_id=video_file)
        #print("dataset is present")

    else:
    # Create a new dataset if it doesn't exist
        dataset = client.create_dataset(name=dataset_name)
        file_path = os.path.join(VIDEO_FOLDER, video_file)
        data_row = dataset.create_data_row(row_data=file_path,external_id=video_file)
        
#print(dataset)
 

