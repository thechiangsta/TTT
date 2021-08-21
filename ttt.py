# Author: Clifton Chiang
# Date: 04/03/2021

import email.utils
import re
import os
import math
import smtplib
import random
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


if __name__ == '__main__':
    senderEmail = '' # Sender's email address 
    password = '' # App password 
    recipients = {}
    # Read the recipients file and extract the email,
    # password, and recipients
    with open('recipients.txt', 'rt') as file:
        for line in file:
            if(line.startswith('email')):
                senderEmail = re.search('\"(\S+@\S+)\"', line)[0]
            elif(line.startswith('password')):
                password = re.search('\"(.+?)\"', line)[0]
            elif(not line.startswith('//') and not line == '\n'):
                matches = re.search('^([0-9]+@[A-Za-z.]+),\W*(\S+)$', line)
                recipients[matches[2].strip()] = matches[1].strip()
    
        
    # The rules of TTT state that generally the number of
    # detectives, traitors, and innocents are percentages
    # of the total number of players.
    # https://trouble-in-terrorist-town.fandom.com/wiki/Detective#:~:text=The%20Detectives%20are%20the%20smallest,out%20who%20the%20Traitors%20are.
    numRoles = len(recipients)
    numDetectives = round(numRoles * 0.125)
    numTraitors = round(numRoles * 0.25)
    numInnocents = round(numRoles * 0.625)
    
    # Fill the roles array with correct number of detectives, traitors, and innocents
    # 0 - Detective
    # 1 - Traitor
    # 2 - Innocent
    roles = []
    for i in range(numDetectives):
        roles.append(0)
    for i in range(numTraitors):
        roles.append(1)
    for i in range(numInnocents):
        roles.append(2)    

    # Ensure the roles are randomized for the players
    random.shuffle(roles)

    # Determine who is what role
    detective = [name for i, (name, phoneNum) in enumerate(recipients.items()) if roles[i] == 0]
    traitors = [name for i, (name, phoneNum) in enumerate(recipients.items()) if roles[i] == 1]
    innocents = [name for i, (name, phoneNum) in enumerate(recipients.items()) if roles[i] == 2]
  
    # The message that will be sent to everyone
    generalMsg = ('\r\n%s is the detective!' % detective[0])

    # Start tls session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(senderEmail, password)

    # Detective
    recipient = recipients[detective[0]]
    body = '\r\nYou are the detective!'
    s.sendmail(senderEmail, recipient, body)

    # Traitors
    for traitor in traitors:
        recipient = recipients[traitor]
        body = generalMsg + '\r\nYou are a traitor! Here are your fellow traitors:\r\n' + \
            ', '.join([v for i, v in enumerate(traitors) if v != traitor])
        s.sendmail(senderEmail, recipient, body)
        

    # Innocents
    for innocent in innocents:
        recipient = recipients[innocent]
        body = generalMsg + '\r\nYou are an innocent!'
        s.sendmail(senderEmail, recipient, body)

    # End session
    s.quit()

