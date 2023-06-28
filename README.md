# Video_Extraction_project
This project tries to extract the videos containing alerts.
There are two main steps for this project:
  1.To download curl logs for specified sensors and mentioned dates.
  2.To download videos with help of curl logs and clip them.
Step2:
  1.Create folder video_download_project on your desktop.
  2.Clone this repo into the folder.
  3.Try running run_with_each_line.It tries to download video based on information in each line.
  4.Video will be downloaded in path ./Desktop/reframed-video
  5.If format of videos is other than mp4.First convert those videso to mp4.
  6.Use python_sdk to upload vidoes to catalog in labelbox.This python_sdk will create a dataset for a sensor if it doesn't exist and upload videos into it.If there 
  is a datset for the specified sensor then it wll just upload the videos to that datset.
  7.And now run create_batches_in_labelbox_videos to create a batch for all the uploaded videos so labellers can start working on it.

