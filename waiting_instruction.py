import os

# Required to read and search email
import email
import imaplib

# Required to send email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Use to upload attachment file
#from email.mime.base import MIMEBase
#from email import encoders

import getpass
import time

from pyautogui import *
import keyboard

# This is to run my alarm-volume-control app internally
# script to turn alarm clock on
def alarmon():
    hotkey("win","r")
    typewrite("cmd")
    press("enter")
    # set delay because computer may lag when running script
    typewrite(" ", interval=4)
    # use keyboard module because it cannot type : symbol
    keyboard.write("d:")
    press("enter")
    keyboard.write('cd "D:\\Python Projects\\Alarm_clock\\alarm_app"')
    press("enter")
    typewrite("activate alarm")
    press("enter")
    typewrite("python main.py")
    press("enter")
    typewrite("60")
    press("enter")
    typewrite("abcde")
    press("enter")
    typewrite("06")
    press("enter")
    typewrite("20")
    press("enter")

def script():
    # Read and search email
    mail.select("inbox")
    # multiple search (yet to be tested): '(OR (TO "tech163@fusionswift.com") (FROM "tech163@fusionswift.com"))'

    result, data = mail.uid("search",'(UNSEEN FROM "myemail@gmail.com")')
    inbox_item_list = data[0].split()
    try:
        most_recent = inbox_item_list[-1]
        result2, email_data = mail.uid('fetch', most_recent, '(RFC822)')
        raw_email = email_data[0][1].decode("utf-8")
        email_message = email.message_from_string(raw_email)
        from_ = email_message['From']
        subject_ = email_message['Subject']
        print("\n Email received from {}!".format(from_))
        print("You have made a request for {}!".format(subject_))
        # remove if condition to do autoreply without running script
        if subject_ == "alarmon":
            to_email = from_
            subject = "Auto reply from Terence's computer"

            msg = MIMEMultipart()
            msg["From"] = username
            msg["To"] = to_email

            msg["Subject"] = subject
            emails = to_email

            body =  "Your request {} has been activated!!".format(subject_)

            msg.attach(MIMEText(body, "plain"))

            text = msg.as_string()
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login(username, password)

            server.sendmail(username,emails,text)
            print("\n Email sent to %s!\n" % from_)
				
            # run script to turn alarm-volume-control app on with desired settings
            alarmon()
    except:
        pass
    time.sleep(5)

if __name__ == "__main__":
    print("\n Wait for new orders...")
    while 1:	
        ###Login###
        username = os.environ.get("my_email")
        password = os.environ.get("my_email_password")

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)

        # input scripts here to automate upon receiving your email instruction
        script()
