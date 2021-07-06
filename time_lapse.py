from datetime import datetime, date, timedelta
import time
import random
import os

import cv2
import moviepy.editor as mpe

from pydrive2.auth import GoogleAuth, ServiceAccountCredentials
from pydrive2.drive import GoogleDrive
from pydub import AudioSegment

from Google import Create_Service
from googleapiclient.http import MediaFileUpload

gauth = GoogleAuth()
scope = ["https://www.googleapis.com/auth/drive"]
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name("****", scope)
drive = GoogleDrive(gauth)

def get_folder_id(parent_id, timeframe):
    folder_list = drive.ListFile({'q':f"mimeType='application/vnd.google-apps.folder' and trashed = false and parents in '{parent_id}'"}).GetList()
    folders     = []
    for folder in folder_list:
        if folder["title"] == str(timeframe):
            folders.append(folder["id"])
    return folders

def folders(parent_id):
    folder_list = drive.ListFile({'q':f"mimeType='application/vnd.google-apps.folder' and trashed = false and parents in '{parent_id}'"}).GetList()
    folders     = []
    for folder in folder_list:
        folders.append(folder["title"])
    return folder

def get_images(google_folder):
    for i in google_folder:
        filename = f"{i['title']}.jpg"
        filenames.append(filename)
        file_instance = drive.CreateFile({"id":i["id"] })
        file_instance.GetContentFile(filename)

def load_images_from_folder(filenames):
    images = []
    for filename in filenames:
        try:
            img = cv2.imread(f"/home/scripts/weather_station/{filename}")
            if img is not None:
                images.append(img)
        except Exception as e:
            print(e)
            continue
    return images

today     = date.today()
yesterday = today - timedelta(days = 1)
month     = datetime.now().strftime('%B')
year      = datetime.now().strftime('%Y')
weather_station = "**************"
year_folder_id  = get_folder_id(weather_station, year)
month_folder_id = get_folder_id(year_folder_id[0], month)
day_folder_id   = get_folder_id(month_folder_id[0], yesterday)

google_folder = drive.ListFile({'q':f"'{day_folder_id[0]}' in parents and trashed=false"}).GetList()
filenames     = []

get_images(google_folder)
images                = load_images_from_folder(filenames)
number_of_images      = len(images)
frame                 = images[0]
height, width, layers = frame.shape
size = (width,height)
print(f"Number of Images: {number_of_images}")

select_song = random.choice(os.listdir("/home/scripts/weather_station/music"))
pydub_song  = AudioSegment.from_mp3(f"/home/scripts/weather_station/music/{select_song}")
song_length = pydub_song.duration_seconds

frame_duration = song_length / number_of_images

out = cv2.VideoWriter(f'ws-{yesterday}-temp.mp4',cv2.VideoWriter_fourcc(*'mp4v'), frame_duration, size)

for i in range(len(images)):
    out.write(images[i])
out.release()

print("Time Lapse Created")

print(f"Song Selected: {select_song}")

audio = mpe.AudioFileClip(f"/home/scripts/weather_station/music/{select_song}")
video = mpe.VideoFileClip(f"/home/scripts/weather_station/ws-{yesterday}-temp.mp4")
final = video.set_audio(mpe.AudioFileClip(f"/home/scripts/weather_station/music/{select_song}"))
final.write_videofile(f"ws-{yesterday}-vid.mp4")

print("Video Created")

video = drive.CreateFile({'title': f'ws-{yesterday}-vid', 'parents': [{'id': f"{day_folder_id[0]}"}]})  
video.SetContentFile(f"/home/scripts/weather_station/ws-{yesterday}-vid.mp4")
video.Upload()
print(f"Upload Successful at {datetime.now()}")

CLIENT_SECRET_FILE = '****'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

upload_date_time = str(date.today())

request_body = {
    'snippet': {
        'categoryI': 19,
        'title': f'24 Hour Time Lapse of the Sky {yesterday}',
        'description': f'24 hour time lapse of the sky with relaxing music. The song is {select_song}. Pictures are taken every 5 minutes.',
        'tags': ['Travel', 'video test', 'Travel Tips']
    },
    'status': {
        'privacyStatus': 'private',
        'publishAt': upload_date_time,
        'selfDeclaredMadeForKids': False, 
    },
    'notifySubscribers': False
}

mediaFile = MediaFileUpload(f'/home/scripts/weather_station/ws-{yesterday}-vid.mp4')

response_upload = service.videos().insert(
    part='snippet,status',
    body=request_body,
    media_body=mediaFile
).execute()

try :
    os.remove(f"/home/scripts/weather_station/ws-{yesterday}-temp.mp4")
    os.remove(f"/home/scripts/weather_station/ws-{yesterday}-vid.mp4")
except Exception as e:
    print(e)

for filename in filenames:
    os.remove(f"/home/scripts/weather_station/{filename}")

print("files removed")
print("done")