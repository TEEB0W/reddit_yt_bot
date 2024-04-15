# import subprocess
import redditscraper
import fetch
import combine
import os
import time
from config import CLIENT_PATH
from youtube_upload.client import YoutubeUploader

DIRECTORY = r'.\REDDIT_YT_BOT\processed_media'


def UploadVideo(file_path,title):
    uploader = YoutubeUploader(secrets_file_path=CLIENT_PATH)
    uploader.authenticate()

    # Video options
    options = {
        "title" : title, # The video title
        "description" : "1", # The video description
        "tags" : ["tag1", "tag2", "tag3"],
        "categoryId" : "22",
        "privacyStatus" : "public", # Video privacy. Can either be "public", "private", or "unlisted"
        "kids" : False, # Specifies if the Video if for kids or not. Defaults to False.
    # "thumbnailLink" : "https://cdn.havecamerawilltravel.com/photographer/files/2020/01/youtube-logo-new-1068x510.jpg" # Optional. Specifies video thumbnail.
    }

    # upload video
    i = uploader.upload(file_path, options,-1) 
    if i[0]['status']['uploadStatus'] == 'uploaded':
        upload_status = True
    uploader.close()
    return upload_status



redditscraper.main()

while True:
    success = fetch.main() #check if urls were retrieved properly
    if success:
        
        break
    else:
        
        redditscraper.main() #if not, retry scrape

combine.main()

auto_upload = input("Should program auto upload to yt (y/n)")
if auto_upload.upper() == 'Y':
#    Cycle through each file in the directory
    for filename in os.listdir(DIRECTORY):
        title =+ 2
        upload_status = UploadVideo(DIRECTORY + "\\" + filename, title)
        if not upload_status:
            break
        time.sleep(8)