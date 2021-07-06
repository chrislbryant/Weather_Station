import smtplib
import os
 
SMTP_SERVER = 'smtp.gmail.com' 
SMTP_PORT = 587 
GMAIL_USERNAME = os.environ.get("GMAIL_USERNAME")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")
 
class Emailer:
    """ This allows the weather station to email """
    def sendmail(self, recipient, subject, content):
         
        headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                   "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)
 
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
 
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
 
        session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        session.quit