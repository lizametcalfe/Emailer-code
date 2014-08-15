import smtplib
from smtplib import SMTP
import time
import datetime
from datetime import date
from time import strptime
import csv
import pandas as pd

count_waitrose_OLD = pd.read_csv('/home/mint/longditudal/output/KPIs/waitrose/dailycounts.csv')
print 'rb test', count_waitrose_OLD
string_attempt = str(count_waitrose_OLD.head(7))

todays_date = datetime.date.strftime(date.today(), '%Y%m%d')

fromaddr = 'onsbigdata@gmail.com'
toaddrs = ['ben.clapperton@ons.gsi.gov.uk','ben.clapperton@hotmail.co.uk','rwb0000@gmail.com', 'robert.breton@ons.gsi.gov.uk'] #'nigel.swier@ons.gsi.gov.uk',
subject = str("Newport: Waitrose Count 7 day")
msg = 'Subject: %s\n\n' % subject + str("Newport scraper: Please find below, the count for the latest 7 days of Waitrose data")+string_attempt
#Credentials
username = 'onsbigdata'
password = 'nibelung14'
# The actual mail send  
server = smtplib.SMTP('smtp.gmail.com:587')  
server.starttls()  
server.login(username,password)  
server.sendmail(fromaddr, toaddrs, msg)  
server.quit()  


count_sainsbury_OLD = pd.read_csv('/home/mint/longditudal/output/KPIs/sainsbury/dailycounts.csv')
string_attempt = str(count_sainsbury_OLD.head(7))

todays_date = datetime.date.strftime(date.today(), '%Y%m%d')

fromaddr = 'onsbigdata@gmail.com'
toaddrs = ['ben.clapperton@ons.gsi.gov.uk','ben.clapperton@hotmail.co.uk','rwb0000@gmail.com', 'robert.breton@ons.gsi.gov.uk'] #'nigel.swier@ons.gsi.gov.uk',
subject = str("Newport: sainsbury Count 7 day")
msg = 'Subject: %s\n\n' % subject + str("Newport scraper: Please find below, the count for the latest 7 days of sainsbury data")+string_attempt
#Credentials
username = 'onsbigdata'
password = 'nibelung14'
# The actual mail send  
server = smtplib.SMTP('smtp.gmail.com:587')  
server.starttls()  
server.login(username,password)  
server.sendmail(fromaddr, toaddrs, msg)  
server.quit() 


count_tesco_OLD = pd.read_csv('/home/mint/longditudal/output/KPIs/tesco/dailycounts.csv')
string_attempt = str(count_tesco_OLD.head(7))

todays_date = datetime.date.strftime(date.today(), '%Y%m%d')

fromaddr = 'onsbigdata@gmail.com'
toaddrs = ['ben.clapperton@ons.gsi.gov.uk','ben.clapperton@hotmail.co.uk','rwb0000@gmail.com', 'robert.breton@ons.gsi.gov.uk'] #'nigel.swier@ons.gsi.gov.uk',
subject = str("Newport: tesco Count 7 day")
msg = 'Subject: %s\n\n' % subject + str("Newport scraper: Please find below, the count for the latest 7 days of tesco data")+string_attempt
#Credentials
username = 'onsbigdata'
password = 'nibelung14'
# The actual mail send  
server = smtplib.SMTP('smtp.gmail.com:587')  
server.starttls()  
server.login(username,password)  
server.sendmail(fromaddr, toaddrs, msg)  
server.quit() 

#['ben.clapperton@ons.gsi.gov.uk','ben.clapperton@hotmail.co.uk','rwb0000@gmail.com', 'robert.breton@ons.gsi.gov.uk']