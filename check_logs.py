from datetime import date, datetime, timedelta
from send_email import Emailer
import os

emailer = Emailer()
today   = date.today()
now     = datetime.now()
previous_minute = (now - timedelta(minutes=1)).strftime("%H:%M")

def did_picture_upload():
    with open(f"/home/pi/Desktop/logs/camera/cron-{today}_{previous_minute}.log") as f:
        data = f.read()
        print(data)
        if "picture_uploaded" in data:
            os.remove(f"/home/pi/Desktop/logs/camera/cron-{today}_{previous_minute}.log")
        else:
            recipient = "chrislbryant83@gmail.com"
            subject = "weatherpi camera"
            content = data
            emailer.sendmail(recipient, subject, content)

def did_data_upload():
    with open(f"/home/pi/Desktop/logs/send_data/cron-{today}_{previous_minute}.log") as f:
        data = f.read()
        print(data)
        if "data_uploaded" in data:
            os.remove(f"/home/pi/Desktop/logs/send_data/cron-{today}_{previous_minute}.log")
        else:
            recipient = "chrislbryant83@gmail.com"
            subject = "weatherpi data"
            content = data
            emailer.sendmail(recipient, subject, content)

def main():
    did_picture_upload()
    did_data_upload()

if __name__ == "__main__":
    main()