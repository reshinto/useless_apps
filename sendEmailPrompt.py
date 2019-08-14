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
# Use this to manually type password
# password = getpass.getpass("Password: ")

# To email input
to_email = []
i = 0
while 1:
    i += 1
    toemail = input("To address %d: " % i)
    if toemail == "":
        break
    to_email.append(toemail)
	
# cc email input
cc_email = []
i = 0
while 1:
    i += 1
    ccemail = input("cc address %d: " % i)
    if ccemail == "":
        break
    cc_email.append(ccemail)

# bcc email input
bcc_email = []
i = 0
while 1:
    i += 1
    bccemail = input("bcc address %d: " % i)
    if bccemail == "":
        break
    bcc_email.append(bccemail)

# subject input
subject = input("Subject: ")

msg = MIMEMultipart()
msg["From"] = username
msg["To"] = ', '.join(to_email)
msg["cc"] = ', '.join(cc_email)
# Not required for bcc
# msg["bcc"] = ', '.join(bcc_email)
msg["Subject"] = subject
emails = to_email + cc_email + bcc_email

# Input main body text here instead of typing while running programn
# Reason is because, return key is not implemented yet, and you can't format your writing
body =  input("text:\n")

msg.attach(MIMEText(body, "plain"))
upload = input("Do you want to attach a file? y/n: ")
if upload == "y" or upload == "Y":
    filename = input("Type filename (including extensions): ")
    attachment = open(filename, "rb")

    part = MIMEBase("application", "octet-stream")
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename= " + filename)

    msg.attach(part)
else:
    pass

text = msg.as_string()
server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(username, password)

server.sendmail(username,emails,text)
print("\n Email sent!\n")
server.quit()
