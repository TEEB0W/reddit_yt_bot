from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip
import moviepy.video.fx.resize
from config import DOWNLOADED_MEDIA
from config import PROCESSED_MEDIA
import os

#TO DO: change how files are retrieved
'''make while loop and add 1 every time the subsequent required file is found'''
def main():
    files = os.listdir(DOWNLOADED_MEDIA) 
    files.sort()
    for i in range(0,len(files)):     #loops through files,every 2nd file assumed to be audio; need to be changed
        if "AUDIO" in files[i]: #if the first char of both files are same they get combined
            continue 
        else:
            if i == len(files) - 1:
                break
            video = VideoFileClip(DOWNLOADED_MEDIA+"\\"+files[i])
            if files[i][0] == files[i+1][0]:
                video.audio = AudioFileClip(DOWNLOADED_MEDIA+"\\"+files[i+1])
            else:
                print("ERROr: audio not found "+ str(files[i]))
                
                
            video.write_videofile(PROCESSED_MEDIA+"\\"+str(files[i]))
        
    return True

if __name__ == "__main__":
    main()
"""file_index = files[i][0]
        next_file= files[i+1]
        if file_index == next_file[0]: #if the first char of both files are same they get combined
            video = VideoFileClip(DOWNLOADED_MEDIA+"\\"+files[i])
            video.audio = AudioFileClip(DOWNLOADED_MEDIA+"\\"+next_file)
            video.write_videofile(PROCESSED_MEDIA+"\\"+str(file_index)+"_combined.mp4")
        else:
            print("ERROr: audio/video not found "+ str(file_index))"""