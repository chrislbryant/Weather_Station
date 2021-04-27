from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive
from picamera import PiCamera
import psycopg2
import datetime
import time
import os

# Take a picture and store it locally
camera       = PiCamera()
now          = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
camera.capture(f"/home/pi/Desktop/pics/ws{now}.jpg")
camera.close()

gauth = GoogleAuth()
scope = ["https://www.googleapis.com/auth/drive"]
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name("/home/pi/Desktop/Projects/weather_station/JSON_FILE.json", scope)
drive = GoogleDrive(gauth)

#----------------------------#
# Set connection credentials #
#----------------------------#
HOST="localhost"
DB="pi"
USER="pi"
PSWD="0623Tiff"

#-------------------------------------#
# Get connected and create a 'cursor' #
#-------------------------------------#
try:
    connection = psycopg2.connect(host=HOST,database=DB,user=USER,password=PSWD)
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    exit()
cursor = connection.cursor()

def get_folder_id(title):
    """ Retrieves current id from DB """
    sql_stmt = f"""
    SELECT {title}
    FROM folders
    WHERE id = 1 
    ; """
    try:
        cursor.execute(sql_stmt)
    except (Exception, psycopg2.Error) as error :
        print ("DB Error: Select * from folders", error)
        print(sql_stmt)
        exit()
    try:
        result = cursor.fetchone()
    except (Exception, psycopg2.Error) as error :
        print ("DB Error: Fetch all rows - folders table", error)
        print(sql_stmt)
        exit()

    return result[0]

def update_folder_id(new_id, title):
    """ Update current id in DB """
    update_id = (new_id,)
    sql_stmt = f"""
        UPDATE folders
        SET {title} = %s
        WHERE id = 1
        ; """
    try:
        cursor.execute(sql_stmt, update_id)
    except (Exception, psycopg2.Error) as error :
        print ("DB Error: Insert into folders", error)
        print(sql_stmt)
        exit()
    connection.commit()

def folders(parent_id):
    """" Get list of google drive folders """
    folder_list = drive.ListFile({'q':f"mimeType='application/vnd.google-apps.folder' and trashed = false and parents in '{parent_id}'"}).GetList()
    folders = []
    for folder in folder_list:
        folders.append(folder["title"])
    return folders

#--------------------------------------------#
# Google Drive Folder and Picture Management #
#--------------------------------------------#

today = datetime.date.today()
month = datetime.datetime.now().strftime('%B')
year  = year = datetime.datetime.now().strftime('%Y')
weather_station_folder_id = get_folder_id("weather_station")
year_folder_id = get_folder_id("year")
month_folder_id = get_folder_id("month")
day_folder_id = get_folder_id("day")

if not str(year) in folders(weather_station_folder_id):
    folder = drive.CreateFile({'title' : f"{year}", 'parents': [{'id': f'{weather_station_folder_id}'}] , 
                            'mimeType' : 'application/vnd.google-apps.folder'})
    folder.Upload()
    new_id = folder["id"]
    update_folder_id(new_id, "year")

if not str(month) in folders(year_folder_id):
    folder = drive.CreateFile({'title' : f"{month}", 'parents': [{'id': f'{year_folder_id}'}] , 
                            'mimeType' : 'application/vnd.google-apps.folder'})
    folder.Upload()
    new_id = folder["id"]
    update_folder_id(new_id, "month")

if not str(today) in folders(f"{month_folder_id}"):
    folder = drive.CreateFile({'title' : f"{today}", 'parents': [{'id': f'{month_folder_id}'}] , 
                            'mimeType' : 'application/vnd.google-apps.folder'})
    folder.Upload()
    new_id = folder["id"]
    update_folder_id(new_id, "day")
    image = drive.CreateFile({'title': f'ws{now}', 'parents': [{'id': f"{new_id}"}]})  
    image.SetContentFile(f"/home/pi/Desktop/pics/ws{now}.jpg")
    image.Upload()
    time.sleep(5)
    os.remove(f"/home/pi/Desktop/pics/ws{now}.jpg")

else:
    image = drive.CreateFile({'title': f'ws{now}', 'parents': [{'id': f"{day_folder_id}"}]})  
    image.SetContentFile(f"/home/pi/Desktop/pics/ws{now}.jpg")
    image.Upload()
    time.sleep(5)
    os.remove(f"/home/pi/Desktop/pics/ws{now}.jpg")

cursor.close()
connection.close()

print("picture_uploaded")