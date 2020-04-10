# Import libraries
import email.utils
import re
import os
import smtplib
import random
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if __name__ == '__main__':
    # 0 - Detective
    # 1 - Traitor
    # 2 - Innocent
    # Here you can modify the roles for the game
    roles = [0, 1, 1, 2, 2, 2]
    random.shuffle(roles)

    # Get the sender and recipient information
    sender = "" # Put your email address here
    file = open('phonenumbers.txt')
    recipients = {}
    for line in file:
        recTemp = line.split(',')
        # Ignore lines that start with //
        if(not recTemp[0].startswith('//', 0, 2) and not recTemp[0] == '\n'):
            number = recTemp[0].strip()
            name = recTemp[1].strip()
            recipients[name] = number

    detective = [name for i, (name, phoneNum) in enumerate(recipients.items()) if roles[i] == 0]
    traitors = [name for i, (name, phoneNum) in enumerate(recipients.items()) if roles[i] == 1]
    innocents = [name for i, (name, phoneNum) in enumerate(recipients.items()) if roles[i] == 2]

    generalMsg = ("\r\n%s is the detective!" % detective[0])
    traitorMsg = " Here are all the traitors: " + ', '.join(traitors)

    print('Detective:', detective)
    print('Traitors:', traitors)
    print('Innocents:', innocents)
    # print(recipients)

    # Start tls session
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    password = "" # App password goes here
    s.login(sender, password)

    # Detective
    recipient = recipients[detective[0]]
    body = "\r\nYou are the detective!"
    # print(body)
    s.sendmail(sender, recipient, body)

    # Traitors
    for traitor in traitors:
        recipient = recipients[traitor]
        body = generalMsg + "\r\nYou are a traitor! Here are your fellow traitors:\r\n" + \
            ', '.join([v for i, v in enumerate(traitors) if v != traitor])
        # print(body)
        s.sendmail(sender, recipient, body)
        

    # Innocents
    for innocent in innocents:
        recipient = recipients[innocent]
        body = generalMsg + "\r\nYou are an innocent!"
        # print(body)
        s.sendmail(sender, recipient, body)

    # End session
    s.quit()