#!/usr/bin/python
# -*- coding: utf-8 -*-

# gmail_massive_email_sender

#Made by Julián Caro Linares-jcarolinares@gmail.com

#LICENSE: CC-BY-SA

#Based on the examples of:
# www.pythondiario.com

#Libraries
import os
import time


#Email and server libraries
from email.mime.text import MIMEText
from smtplib import SMTP

#Config  library
import configparser

#List of email

#Open and read the file of emails address
emails_file=open("emails_file.txt")
list_of_emails=emails_file.readlines()

for index in range(len(list_of_emails)):
    list_of_emails[index]=list_of_emails[index].replace("\n","")

#list_of_emails=["defaultemail@gmail.com","defaultemail@gmail.com","defaultemail@gmail.com","defaultemail@gmail.com"]

class gmail_account:
    def new(self,user,password):
        self.password=str(password)
        self.user=str(user)
    def get_user(self):
        return self.user
    def get_password(self):
        return self.password

class email:
    def new(self,from_address, to_address,subject, message):
        self.from_address=str(from_address)
        self.to_address=str(to_address)
        self.subject=str(subject)
        self.message=str(message)
    def get_from_address(self):
        return self.from_address
    def get_to_address(self):
        return self.to_address
    def get_subject(self):
        return self.subject
    def get_message(self):
        return self.message

def main():

    #User data
    print ("[+] Reading config file... ")
    print("Done")
    config = configparser.ConfigParser()
    config.read([os.path.expanduser('./config')])

    user=gmail_account()
    user.new(config.get('user_email','user_name'),config.get('user_email','password'))

    #parse email message to include new lines and paragraphs
    message1 = config.get('email_data','message')
    message1.replace('\\n', '\n')

    #Email data
    email_to_send=email()
    email_to_send.new(user.get_user(),"defaultemail@gmail.com",config.get('email_data','subject'),message1)

    #Load of packages control


    counter_factor=1
    for index in range(len(list_of_emails)):
        #Sending the email

        mime_message = MIMEText(email_to_send.get_message())
        #mime_message["From"] = email_to_send.get_from_address()
        mime_message["From"] = user.get_user()
        mime_message["To"] =list_of_emails[index]
        #mime_message["To"] =email_to_send.get_to_address()
        mime_message["Subject"] = email_to_send.get_subject()
        smtp = SMTP("smtp.gmail.com", 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(user.get_user(), user.get_password())
        smtp.sendmail(email_to_send.get_from_address(), list_of_emails[index], mime_message.as_string())
        print("\nEmail sended to: "+list_of_emails[index]+ " from: "+email_to_send.get_from_address())
        smtp.quit()


        if(index>=counter_factor*int(config.get('packages_control','emails_in_package'))-1):
            print ("\nWaiting "+config.get('packages_control','sleeping_time')+" for the next package")
            time.sleep(float(config.get('packages_control','sleeping_time')))
            counter_factor=counter_factor+1

if __name__ == "__main__":
 main()
