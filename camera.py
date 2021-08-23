import os
import time
from datetime import date, datetime

from picamera import PiCamera
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive

from postgres_interface import DatabaseInterface

db    = DatabaseInterface()
gauth = GoogleAuth()
scope = ["https://www.googleapis.com/auth/drive"]
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name("/home/pi/Desktop/Projects/weather_station/JSON_FILE.json", scope)
drive = GoogleDrive(gauth)

NOW   = datetime.now().strftime("%Y-%m-%d-%H-%M")
TODAY = date.today()
MONTH = datetime.now().strftime('%B')
YEAR  = datetime.now().strftime('%Y')

def take_picture():
    """ Take a picture and store it locally """

    camera = PiCamera()
    camera.capture(f"/home/pi/Desktop/pics/ws{NOW}.jpg")
    camera.close()

def get_folder_id(folder_name):
    """ Retrieve a Google foler id from db"""

    query = f"""
        SELECT {folder_name}
          FROM folders
         WHERE id = 1 
    ; """
    result = db.fetch_one(query)
    return result[0]    
        
def update_folder_id(new_folder_id, folder_name):
    """ Update current google folder id in DB """

    query = f"""
        UPDATE folders
           SET {folder_name} = '{new_folder_id}'
         WHERE id = 1
        ; """
    db.execute(query)
    db.commit()

def folders(parent_id):
    """" Get list of Google drive folders """

    folder_list = drive.ListFile({'q':f"mimeType='application/vnd.google-apps.folder' and trashed = false and parents in '{parent_id}'"}).GetList()
    folders = []
    for folder in folder_list:
        folders.append(folder["title"])
    return folders

def create_folder(folder_name, folder_id):
    """ Create a new Google drive folder """

    folder = drive.CreateFile({'title' : f"{folder_name}", 'parents': [{'id': f'{folder_id}'}] , 
                            'mimeType' : 'application/vnd.google-apps.folder'})
    folder.Upload()
    new_folder_id = folder["id"]
    return new_folder_id

def upload_image(now, folder_id):
    """ Upload an image to Google drive folder """

    image = drive.CreateFile({'title': f'ws{NOW}', 'parents': [{'id': f"{folder_id}"}]})  
    image.SetContentFile(f"/home/pi/Desktop/pics/ws{NOW}.jpg")
    image.Upload()
    time.sleep(10)
    os.remove(f"/home/pi/Desktop/pics/ws{NOW}.jpg")

def main():
    if not str(YEAR) in folders(get_folder_id("weather_station")):
        update_folder_id(create_folder(YEAR, get_folder_id("weather_station")), "year")

    if not str(MONTH) in folders(get_folder_id("year")):
        update_folder_id(create_folder(MONTH, get_folder_id("year")), "month")

    if not str(TODAY) in folders(get_folder_id("month")):
        update_folder_id(create_folder(TODAY, get_folder_id("month")), "day")
    
    take_picture()
    upload_image(NOW, get_folder_id("day"))
    db.close()
    print("picture_uploaded")

if __name__ == "__main__":
    main()
    
    