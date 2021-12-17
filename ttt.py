# Author: Clifton Chiang
# Date: 04/03/2021

import json
import re
import smtplib
import random


if __name__ == '__main__':
    with open('recipients.json', 'r') as json_file:
        data = json.load(json_file)

        # Validate data
        if not data.get('sender'):
            raise Exception("Missing sender")
        sender_email = data.get('sender').get('email')
        sender_password = data.get('sender').get('password')
        recipients = data.get('recipients')
        if not sender_email or not re.search('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', sender_email):
            raise Exception("Valid email required")
        if not sender_password:
            raise Exception("Password required")
        if not recipients:
            raise Exception("No recipients added")
        
    # The rules of TTT state that generally the number of
    # detectives, traitors, and innocents are percentages
    # of the total number of players.
    # https://trouble-in-terrorist-town.fandom.com/wiki/Detective#:~:text=The%20Detectives%20are%20the%20smallest,out%20who%20the%20Traitors%20are.
    num_roles = len(recipients)
    num_detectives = round(num_roles * 0.125)
    num_traitors = round(num_roles * 0.25)
    num_innocents = num_roles - num_detectives - num_traitors
    
    # Fill the roles array with correct number of detectives, traitors, and innocents
    roles = []
    for i in range(num_detectives):
        roles.append('detective')
    for i in range(num_traitors):
        roles.append('traitor')
    for i in range(num_innocents):
        roles.append('innocent')    

    # Shuffle the recipients so roles are randomized
    random.shuffle(recipients)
    random.shuffle(roles)

    # Assign the roles to recipients
    for role, recip in zip(roles, recipients):
        recip.update({
            'role': role
        })
    
    # Determine who is what role
    detective = next(r for r in recipients if r.get('role') == 'detective')
    traitors = [r for r in recipients if r.get('role') == 'traitor']
    innocents = [r for r in recipients if r.get('role') == 'innocent']

    # The message that will be sent to everyone
    generalMsg = f"{detective.get('name')} is the detective!"

    # Start tls session
    smtpServer = ''
    emailProvider = re.search('@([A-Za-z]+).com', sender_email).group(1)
    if emailProvider == 'yahoo':
        smtpServer = 'smtp.mail.yahoo.com'
    elif emailProvider == 'gmail':
        smtpServer = 'smtp.gmail.com'
    elif emailProvider == 'aol':
        smtpServer = 'smtp.aol.com'

    s = smtplib.SMTP(smtpServer, 587)
    s.starttls()
    s.login(sender_email, sender_password)

    # Detective
    s.sendmail(sender_email, detective.get('phone'), '\r\nYou are the detective!')

    # Traitors
    for t in traitors:
        s.sendmail(sender_email, t.get('phone'), 
            f"{generalMsg}\r\nYou are a traitor! Here are your fellow traitor(s): {', '.join([tr.get('name') for tr in traitors if tr.get('phone') != t.get('phone')])}"
        )

    # Innocents
    for i in innocents:
        s.sendmail(sender_email, i.get('phone'), f"{generalMsg}\r\nYou are an innocent!")

    # End session
    s.quit()
