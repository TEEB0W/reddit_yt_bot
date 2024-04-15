from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip
import moviepy.video.fx.resize
from config import DOWNLOADED_MEDIA
from config import PROCESSED_MEDIA
import os

def main():
    files = os.listdir(DOWNLOADED_MEDIA) #get files to be combined
    files.sort()
    for i in range(0,len(files)):   
        if "AUDIO" in files[i]: # the program will skip solo audio files
            continue 
        else:
            if i == len(files) - 1:
                break
            video = VideoFileClip(DOWNLOADED_MEDIA+"\\"+files[i])
            if files[i][0] == files[i+1][0]:    #if the first char of both files are same they get combined
                video.audio = AudioFileClip(DOWNLOADED_MEDIA+"\\"+files[i+1])
            else:
                print("ERROr: audio not found "+ str(files[i]))
                
                
            video.write_videofile(PROCESSED_MEDIA+"\\"+str(files[i]))
        
    return True

if __name__ == "__main__":
    main()