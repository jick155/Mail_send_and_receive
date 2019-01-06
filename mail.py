# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 07:16:36 2019

@author: user
"""


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


import os, subprocess
SMTP_SERVER = "***"
SMTP_PORT = 587
SMTP_USERNAME = "***"
SMTP_PASSWORD = "***"
EMAIL_FROM = "***"
EMAIL_TO = "***"
EMAIL_SUBJECT = "REMINDER:"
co_msg = """
Hello, [username]! Just wanted to send a friendly appointment
reminder for your appointment:
[Company]
Where: [companyAddress]
Time: [appointmentTime]
Company URL: [companyUrl]
Change appointment?? Add Service??
change notification preference (text msg/email)
"""
def attach(file,filename1):
    part = MIMEApplication(open( file, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=filename1)
    return part

def send_email(mail,msg):
    
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM 
    msg['To'] = EMAIL_TO
    debuglevel = True
    
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()
    
def check_filesize(path):
    file_val=[]
    arg = 'a'
    file_path , filename = os.path.split(path)
    if os.path.getsize(path)>(1024*1024*15):
        subprocess.call(['7z',arg,filename,path , '-v10m'])
    os.chdir(file_path)
    a=os.listdir('.')
    for i in a:
        if filename in i:
            file_val.append(i)
    return file_val


if __name__ =='__main__':
    path =r'tensorflow 實戰分析.pdf'
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    file_list = check_filesize(path)
    for i in file_list:
        part = attach(i,i)
        msg =MIMEMultipart()
        msg.attach(MIMEText(co_msg))
        msg.attach(part)
        send_email(mail,msg)