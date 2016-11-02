import smtplib
from smtplib import SMTP
import time
import datetime
from datetime import date
from time import strptime
import csv
import pandas as pd
import numpy as np
import scipy as sp
import scipy.stats

count_waitrose_OLD = pd.read_csv('/media/mint/e834712c-23da-4cbe-a4ec-3a35d416877b/my-data/global_code/KPIs/waitrose/dailycounts.csv')
print 'rb test', count_waitrose_OLD
string_attempt = str(count_waitrose_OLD.head(7))

#check if new value is plus or minus 10 percent the previous value
if count_waitrose_OLD["waitroses_count"][0] > count_waitrose_OLD["waitroses_count"][1]*1.1:
    Ten_percent_out_previous = "Check"
elif count_waitrose_OLD["waitroses_count"][0] < count_waitrose_OLD["waitroses_count"][1]*0.9:
    Ten_percent_out_previous = "Check"    
else:
    Ten_percent_out_previous = ""

def mean_confidence_interval(data, confidence):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h

#check if new value is outside the confidence interval of last 50 values. 
L = mean_confidence_interval(count_waitrose_OLD["waitroses_count"].head(50),0.95)[1]
U = mean_confidence_interval(count_waitrose_OLD["waitroses_count"].head(50),0.95)[2]

if count_waitrose_OLD["waitroses_count"][0] > U:
    Outside_conf_int = "Yes"
elif count_waitrose_OLD["waitroses_count"][0] < L:
    Outside_conf_int = "Yes"    
else:
    Outside_conf_int = "No"

todays_date = datetime.date.strftime(date.today(), '%Y%m%d')

fromaddr = 'onsbigdata@gmail.com'
toaddrs = ['rwb0000@gmail.com','lizametcalfe@gmail.com','inboxfolder101@gmail.com', 't.z.lewis@hotmail.com','vidhya12.shekar@gmail.com'] #'nigel.swier@ons.gsi.gov.uk','ben.clapperton@ons.gsi.gov.uk','ben.clapperton@hotmail.co.uk',
subject = str("Newport: Waitrose Count 7 day:")
msg = 'Subject: %s\n\n' % subject + str("Newport scraper: Please find below, the count for the latest 7 days of Waitrose data    10percent out of previous value?:   Outside confidence interval?")+string_attempt+"      "+Ten_percent_out_previous+"     "+Outside_conf_int
#Credentials
username = 'onsbigdata'
password = 'nibelung14'
# The actual mail send  
server = smtplib.SMTP('smtp.gmail.com:587')  
server.starttls()  
server.login(username,password)  
server.sendmail(fromaddr, toaddrs, msg)  
server.quit()  

count_sainsbury_OLD = pd.read_csv('/media/mint/e834712c-23da-4cbe-a4ec-3a35d416877b/my-data/global_code/KPIs/sainsbury/dailycounts.csv')
string_attempt = str(count_sainsbury_OLD.head(7))

#check if new value is plus or minus 10 percent the previous value
if count_sainsbury_OLD["sainsburys_count"][0] > count_sainsbury_OLD["sainsburys_count"][1]*1.1:
    Ten_percent_out_previous = "Check"
elif count_sainsbury_OLD["sainsburys_count"][0] < count_sainsbury_OLD["sainsburys_count"][1]*0.9:
    Ten_percent_out_previous = "Check"    
else:
    Ten_percent_out_previous = ""

#check if new value is outside the confidence interval of last 50 values. 
L = mean_confidence_interval(count_sainsbury_OLD["sainsburys_count"].head(50),0.95)[1]
U = mean_confidence_interval(count_sainsbury_OLD["sainsburys_count"].head(50),0.95)[2]

if count_sainsbury_OLD["sainsburys_count"][0] > U:
    Outside_conf_int = "Yes"
elif count_sainsbury_OLD["sainsburys_count"][0] < L:
    Outside_conf_int = "Yes"    
else:
    Outside_conf_int = "No"

todays_date = datetime.date.strftime(date.today(), '%Y%m%d')

fromaddr = 'onsbigdata@gmail.com'
toaddrs = ['rwb0000@gmail.com','lizametcalfe@gmail.com','inboxfolder101@gmail.com', 't.z.lewis@hotmail.com','vidhya12.shekar@gmail.com'] #'nigel.swier@ons.gsi.gov.uk',
subject = str("Newport: sainsbury Count 7 day:")
msg = 'Subject: %s\n\n' % subject + str("Newport scraper: Please find below, the count for the latest 7 days of sainsbury data.    10percent out of previous value?:   Outside confidence interval?")+string_attempt+"     "+Ten_percent_out_previous+"     "+Outside_conf_int
#Credentials
username = 'onsbigdata'
password = 'nibelung14'
# The actual mail send  
server = smtplib.SMTP('smtp.gmail.com:587')  
server.starttls()  
server.login(username,password)  
server.sendmail(fromaddr, toaddrs, msg)  
server.quit() 


count_tesco_OLD = pd.read_csv('/media/mint/e834712c-23da-4cbe-a4ec-3a35d416877b/my-data/global_code/KPIs/tesco/dailycounts.csv')
string_attempt = str(count_tesco_OLD.head(7))


#check if new value is plus or minus 10 percent the previous value
if count_tesco_OLD["tescos_count"][0] > count_tesco_OLD["tescos_count"][1]*1.1:
    Ten_percent_out_previous = "Check"
elif count_tesco_OLD["tescos_count"][0] < count_tesco_OLD["tescos_count"][1]*0.9:
    Ten_percent_out_previous = "Check"    
else:
    Ten_percent_out_previous = ""

#check if new value is outside the confidence interval of last 50 values. 
L = mean_confidence_interval(count_tesco_OLD["tescos_count"].head(50),0.95)[1]
U = mean_confidence_interval(count_tesco_OLD["tescos_count"].head(50),0.95)[2]

if count_tesco_OLD["tescos_count"][0] > U:
    Outside_conf_int = "Yes"
elif count_tesco_OLD["tescos_count"][0] < L:
    Outside_conf_int = "Yes"    
else:
    Outside_conf_int = "No"

todays_date = datetime.date.strftime(date.today(), '%Y%m%d')

fromaddr = 'onsbigdata@gmail.com'
toaddrs = ['rwb0000@gmail.com','lizametcalfe@gmail.com','inboxfolder101@gmail.com', 't.z.lewis@hotmail.com','vidhya12.shekar@gmail.com'] #'nigel.swier@ons.gsi.gov.uk',
subject = str("Newport: tesco Count 7 day:")
msg = 'Subject: %s\n\n' % subject + str("Newport scraper: Please find below, the count for the latest 7 days of tesco data    10percent out of previous value?:   Outside confidence interval?")+string_attempt+"     "+Ten_percent_out_previous+"     "+Outside_conf_int
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
