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

#calculate whether the new count is within the confidence interval of the last fifty counts
def mean_confidence_interval(data, confidence):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h

def conf(data, confidence, data_var, today):
    #check if new value is outside the confidence interval of last 50 values. 
    L = mean_confidence_interval(data[data_var].head(50),0.95)[1]
    U = mean_confidence_interval(data[data_var].head(50),0.95)[2]
    if today > U:
        return "Above confidence interval"
    elif today < L:
        return "Below confidence interval"    
    else:
        return ""

#calculate whether the new count is within the confidence interval of the last fifty counts and add to email resutls
count_waitrose_OLD["Confidence_interval"] = ""
count_waitrose_OLD["Confidence_interval"][0] = conf(count_waitrose_OLD,0.95,"waitroses_count",count_waitrose_OLD["waitroses_count"][0])

string_attempt = str(count_waitrose_OLD.head(7))


todays_date = datetime.date.strftime(date.today(), '%Y%m%d')

fromaddr = 'onsbigdata@gmail.com'
toaddrs = ['lizametcalfe@gmail.com'] #'nigel.swier@ons.gsi.gov.uk','ben.clapperton@ons.gsi.gov.uk','ben.clapperton@hotmail.co.uk',
subject = str("Newport: Waitrose Count 7 day:")
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

count_sainsbury_OLD = pd.read_csv('/media/mint/e834712c-23da-4cbe-a4ec-3a35d416877b/my-data/global_code/KPIs/sainsbury/dailycounts.csv')

#calculate whether the new count is within the confidence interval of the last fifty counts and add to email resutls
count_sainsbury_OLD["Confidence_interval"] = ""
count_sainsbury_OLD["Confidence_interval"][0] = conf(count_sainsbury_OLD,0.95,"sainsburys_count",count_sainsbury_OLD["sainsburys_count"][0])

string_attempt = str(count_sainsbury_OLD.head(7))

todays_date = datetime.date.strftime(date.today(), '%Y%m%d')

fromaddr = 'onsbigdata@gmail.com'
toaddrs = ['lizametcalfe@gmail.com'] #'nigel.swier@ons.gsi.gov.uk',
subject = str("Newport: sainsbury Count 7 day:")
msg = 'Subject: %s\n\n' % subject + str("Newport scraper: Please find below, the count for the latest 7 days of sainsbury data.")+string_attempt
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
#calculate whether the new count is within the confidence interval of the last fifty counts and add to email resutls
count_tesco_OLD["Confidence_interval"] = ""
count_tesco_OLD["Confidence_interval"][0] = conf(count_tesco_OLD,0.95,"tescos_count",count_tesco_OLD["tescos_count"][0])

string_attempt = str(count_tesco_OLD.head(7))

todays_date = datetime.date.strftime(date.today(), '%Y%m%d')

fromaddr = 'onsbigdata@gmail.com'
toaddrs = ['lizametcalfe@gmail.com'] #'nigel.swier@ons.gsi.gov.uk',
subject = str("Newport: tesco Count 7 day:")
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
