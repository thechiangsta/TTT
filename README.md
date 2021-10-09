# TTT Roles Generator
---

### Purpose
For you and friends to be able to play [Trouble in Terrorist Town](https://www.troubleinterroristtown.com/) whether in person or in a video game that doesn't already have some in-game support for TTT. With this generator you will be able to use your Gmail account (no support for other emails as of now) to send the players' roles via SMS messages.

### Setup
1. Ensure you have Python installed. If you do not, you can do so [here](https://www.python.org/downloads/).
2. You'll need to create an app password for your Google account to use for sending the messages to other players.<br>
   1. Navigate to your Google account security [settings](https://myaccount.google.com/intro/security) and under the **Signing in to Google** section, click **App passwords**.
   2. Click the **Select app** dropdown and choose **Other**. You will be prompted to name the password.
   3. Copy the password as you will not be able to retrieve it; and if lost, you will have to create a new password.
   <br>
   <br>
  ![Google App Passwords](images/apppasswords.png)
  <br>
  <br>
  <br>

### Helpful Info
Here are the SMS gateway domains for popular providers (U.S.) you might need:
*  Alltel - sms.alltelwireless.com
*  AT&T - txt.att.net
*  Boost Mobile - sms.myboostmobile.com
*  Cricket Wireless - mms.cricketwireless.net
*  FirstNet - tzt.att.net
*  Metro PCS - mymetropcs.com
*  Republic Wireless - text.republicwireless.com
*  Sprint - messaging.sprintpcs.com
*  T-Mobile - tmomail.net
*  U.S. Cellular - email.uscc.net
*  Verizon - vtext.com
*  Virgin Mobile - vmobl.com

### Usage
1. Enter your email and app password in the **recipients.json** file in the **sender** object fields **email** and **password** respectively.
2. Add the recipients' phone number and name in the **recipients** array. Ensure to format the recipients' **phone** field as: \<phone-number\>@\<sms-gateway\>. An example is given to you in the file.
3. Run the Python script with the command: **python ttt.py**