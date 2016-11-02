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

#functions for checks

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
        return "Above confidence interval range - check!"
    elif today < L:
        return "Below confidence interval range - check!"    
    else:
        return ""

#check individual products for big changes over time
def checkzero(itemdata):
    for i in itemdata.columns:
        itemdata=itemdata.rename(columns = {i:i.replace("_","")})
    itemdata2 = pd.DataFrame()
    itemdata2["Zero Products collected for the following items:"] = itemdata.apply(lambda x: x["ONSITEMNAME"] if x[todays_date] == 0 else "non",axis=1)
    return str(itemdata2[itemdata2["Zero Products collected for the following items:"]!="non"])

def checkbig(itemdata):
    for i in itemdata.columns:
        itemdata=itemdata.rename(columns = {i:i.replace("_","")})
    itemdata3 = pd.DataFrame()
    itemdata3["Large difference to mean for the following items:"] = itemdata.apply(lambda x: x["ONSITEMNAME"] if abs(x["Dif:TODAY-7DAYMEAN"]) > 30 else "non",axis=1)
    return str(itemdata3[itemdata3["Large difference to mean for the following items:"]!="non"])

count_waitrose_OLD = pd.read_csv('/media/mint/e834712c-23da-4cbe-a4ec-3a35d416877b/my-data/global_code/KPIs/waitrose/dailycounts.csv')
print 'rb test', count_waitrose_OLD


#calculate whether the new count is within the confidence interval of the last fifty counts and add to email resutls
count_waitrose_OLD["Confidence_interval"] = ""
count_waitrose_OLD["Confidence_interval"][0] = conf(count_waitrose_OLD,0.95,"waitroses_count",count_waitrose_OLD["waitroses_count"][0])
count_waitrose_OLD=count_waitrose_OLD.rename(columns = {'Unnamed: 0':''})

string_attempt_waitrose = str(count_waitrose_OLD.head(7))

todays_date = datetime.date.strftime(date.today(), '%Y%m%d')

#Check whether there are any items where zero products are collected

itemdata_waitrose = pd.read_csv("/media/mint/e834712c-23da-4cbe-a4ec-3a35d416877b/my-data/global_code/KPIs/waitrose/waitrose_item_counts.csv")
#Check whether there is a big change from the mean (for last seven days), or zero products
Waitrose_zero = checkzero(itemdata_waitrose)
Waitrose_big = checkbig(itemdata_waitrose)

count_sainsbury_OLD = pd.read_csv('/media/mint/e834712c-23da-4cbe-a4ec-3a35d416877b/my-data/global_code/KPIs/sainsbury/dailycounts.csv')

#calculate whether the new count is within the confidence interval of the last fifty counts and add to email resutls
count_sainsbury_OLD["Confidence_interval"] = ""
count_sainsbury_OLD["Confidence_interval"][0] = conf(count_sainsbury_OLD,0.95,"sainsburys_count",count_sainsbury_OLD["sainsburys_count"][0])
count_sainsbury_OLD=count_sainsbury_OLD.rename(columns = {'Unnamed: 0':''})

string_attempt_sainsbury = str(count_sainsbury_OLD.head(7))

#Check whether there are any items where zero products are collected

itemdata_sainsbury = pd.read_csv("/media/mint/e834712c-23da-4cbe-a4ec-3a35d416877b/my-data/global_code/KPIs/sainsbury/sainsbury_item_counts.csv")
#Check whether there is a big change from the mean (for last seven days), or zero products
Sainsbury_zero = checkzero(itemdata_sainsbury)
Sainsbury_big = checkbig(itemdata_sainsbury)

count_tesco_OLD = pd.read_csv('/media/mint/e834712c-23da-4cbe-a4ec-3a35d416877b/my-data/global_code/KPIs/tesco/dailycounts.csv')
#calculate whether the new count is within the confidence interval of the last fifty counts and add to email resutls
count_tesco_OLD["Confidence_interval"] = ""
count_tesco_OLD["Confidence_interval"][0] = conf(count_tesco_OLD,0.95,"tescos_count",count_tesco_OLD["tescos_count"][0])
count_tesco_OLD=count_tesco_OLD.rename(columns = {'Unnamed: 0':''})

string_attempt_tesco = str(count_tesco_OLD.head(7))

#Check whether there are any items where zero products are collected

itemdata_tesco = pd.read_csv("/media/mint/e834712c-23da-4cbe-a4ec-3a35d416877b/my-data/global_code/KPIs/tesco/tesco_item_counts.csv")
#Check whether there is a big change from the mean (for last seven days), or zero products
Tesco_zero = checkzero(itemdata_tesco)
Tesco_big = checkbig(itemdata_tesco)

fromaddr = 'onsbigdata@gmail.com'
toaddrs = ['lizametcalfe@gmail.com','inboxfolder101@gmail.com', 't.z.lewis@hotmail.com','vidhya12.shekar@gmail.com', 'podscraper@gmail.com', 'shivam_patel123@hotmail.com'] #'nigel.swier@ons.gsi.gov.uk','ben.clapperton@ons.gsi.gov.uk','ben.clapperton@hotmail.co.uk',
subject = str("Newport: Web-scrapers Count 7 day:")
msg = 'Subject: %s\n\n' % subject + str("Newport scraper: Please find below, the count for the latest 7 days of Waitrose data\n")+"\n Waitrose\n"+"\n"+string_attempt_waitrose+"\n"+"\n Quick check of individual items\n"+Waitrose_zero+"\n"+"\n"+Waitrose_big+"\n"+"\n Tesco \n"+"\n"+string_attempt_tesco+"\n"+"\n Quick check of individual items\n"+Tesco_zero+"\n"+"\n"+Tesco_big+"\n"+"\n Sainsbury \n"+"\n"+string_attempt_sainsbury+"\n"+"\n Quick check of individual items\n"+Sainsbury_zero+"\n"+"\n"+Sainsbury_big
#Credentials
username = 'onsbigdata'
password = 'nibelung14'
# The actual mail send  
server = smtplib.SMTP('smtp.gmail.com:587')  
server.starttls()  
server.login(username,password)  
server.sendmail(fromaddr, toaddrs, msg)  
server.quit()  


