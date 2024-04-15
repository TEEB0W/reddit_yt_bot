import urllib.request
from config import API_KEY
from config import MEDIA_URLS_PATH
from config import DOWNLOADED_MEDIA
import requests
from urllib.error import HTTPError
from random import randint

def get_headers_list(): #use headers fom scrapeops
  response = requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=' + API_KEY)
  json_response = response.json()
  return json_response.get('result', [])

def get_random_header(header_list):
  random_index = randint(0, len(header_list) - 1)
  return header_list[random_index]

def loadmedia(url,count,extension,header):
    #if os.path.exists(filename):
    #circumvent 403 error using headers
    filename = str(count)+extension
    
    try:    #catch if a 403 error error occurs while downloading // 403 may happen if the url is not correct
        req = urllib.request.Request(url.strip() +"/DASH"+ extension, headers=header) #downloading
        response = urllib.request.urlopen(req)
        file = open(DOWNLOADED_MEDIA+"\\"+filename, 'wb') #copying media to local
        file.write(response.read())
        file.close()
    except HTTPError as e:
        if e.code == 403:
            return False
    except Exception as e:
        print("downloading ERROR: ",url,e,"|",filename)
    return True

def loadVideo(url, count): #go thru each extension until succesful
    header_list = get_headers_list()

    for extension in ["_360.mp4","_270.mp4","_220.mp4","_480.mp4","_720.mp4","_1080.mp4"]:
        success = loadmedia(url,count,extension,get_random_header(header_list))
        if success:
            break
    else:
        print("Resolution not found 403 ERROR: ",url,str(count) + "_video file")
        

def loadAudio(url, count): #go thru each extension until succesful
    header_list = get_headers_list()

    for extension in ["_AUDIO_64.mp4","_AUDIO_128.mp4"]:
        success = loadmedia(url,count,extension,get_random_header(header_list))
        if success:
            break
        if extension == "_AUDIO_128.mp4" and not success:
            print("Resolution not found 403 ERROR: ",url,str(count) + "_audio file")
            break

def main():
    count = 0 #used for naming, and counting failed urls
    urls = open(MEDIA_URLS_PATH, 'r')
    while True: #read file
        
        url = urls.readline()

        if not url: 
            break
        elif '/r/' in url: # crawler likely malfunctioned if /r/ encountered in url
            print("ERROR: invalid urls, try again ")
            return False
        else:
            count += 1 
        
        loadVideo(url,count) #download from urls
        loadAudio(url,count)

    urls.close()
    return True

if __name__ == "__main__":
    main()
# headers = {
#             "upgrade-insecure-requests": "1",
#             "user-agent": "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
#             "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#             "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
#             "sec-ch-ua-mobile": "?0",
#             "sec-ch-ua-platform": "\"Windows\"",
#             "sec-fetch-site": "none",
#             "sec-fetch-mod": "",
#             "sec-fetch-user": "?1",
#             "accept-encoding": "gzip, deflate, br",
#             "accept-language": "bg-BG,bg;q=0.9,en-US;q=0.8,en;q=0.7"
#         }
    
    #No such file or directory: 'C:\\Users\\Abdulla\\Documents\\coding\\reddit_scrapy\\downloaded_media\\1_360.mp4