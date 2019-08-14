import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Use to upload attachment file
from email.mime.base import MIMEBase
from email import encoders

import getpass

# Login email
username = os.environ.get("my_email")
password = os.environ.get("my_email_password")
# Use the following if you want to type your password before sending
# password = getpass.getpass("Password: ")

# Multiple emails: ["xxx@gmail.com", "yyy@yahoo.com"]
to_email = ["sendemail@gmail.com"] 
cc_email = [] 
bcc_email = ["bccsend@gmail.com"] 
subject = "MY SUBJECT"

msg = MIMEMultipart()
msg["From"] = username
msg["To"] = ', '.join(to_email)
msg["cc"] = ', '.join(cc_email)
#msg["bcc"] = ', '.join(bcc_email)
msg["Subject"] = subject
emails = to_email + cc_email + bcc_email

body = """\
Hi there
"""
msg.attach(MIMEText(body, "plain"))

# Upload file: remove """ """ to attach file
"""
filename = "test.py"
attachment = open(filename, "rb")
part = MIMEBase("application", "octet-stream")
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", "attachment; filename= " + filename)
msg.attach(part)
"""

text = msg.as_string()
server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(username, password)

server.sendmail(username,emails,text)
server.quit()
