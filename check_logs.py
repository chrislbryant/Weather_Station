from datetime import datetime,timedelta, date
from send_email import Emailer
import os

emailer = Emailer()

today = date.today()
now = datetime.now()
previous_minute = (now - timedelta(minutes=1)).strftime("%H:%M")

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