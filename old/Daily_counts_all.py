#Purpose of code:
# Add a new date to the supermarket's daily count
# Get item counts

import pandas as pd
import numpy as np
import matplotlib as mat
import matplotlib.pyplot as plt
import datetime
import csv
import os
import fnmatch
import smtplib

from pandas import groupby
from pandas import DataFrame
from pandas import Series

import time
import datetime
from datetime import date
from time import strptime

#Then next days scrape data
def update_prices_daily_count(supermarket, the_date):
    #read in file with the_date
    filename = str(supermarket+'_products_')+str(the_date)+str('*')
    print filename
    counter = 0
    for file in os.listdir('/home/mint/workinprogress/data_collection/supermarket_scraper/output/'+supermarket+'/'):
        
        if fnmatch.fnmatch(file, filename):
            atpos = file.find('_2')
            stopos = file.find('.')
            time = file[atpos+1:stopos]

            if counter == 0:

                file2 = '/home/mint/workinprogress/data_collection/supermarket_scraper/output/'+supermarket+'/'+ file
                print "file equals ", file2
                time_before = file[atpos+1:stopos]

            elif int(time) > int(time_before):
                file2 = '/home/mint/workinprogress/data_collection/supermarket_scraper/output/'+supermarket+'/'+ file
                time_before = file[atpos+1:stopos]
                print "file equals ", file2

            counter = counter+1

            
    supermarketDaily = pd.read_csv(file2)
    print len(supermarketDaily)
    
    #create date column for use later, using the datetime column
    supermarketDaily["date"] = datetime.datetime.strptime(supermarketDaily["timestamp"][0],"%Y-%m-%d %H:%M:%S.%f").date()
    for i in range(1,len(supermarket)):
        supermarketDaily["date"][i] = datetime.datetime.strptime(supermarketDaily["timestamp"][i],"%Y-%m-%d %H:%M:%S.%f").date()

    
    
    #
    count_supermarket = supermarketDaily['std_price'].groupby([supermarketDaily['date']]).count()
    #       
    daily_count_supermarket = supermarketDaily['std_price'].groupby([supermarketDaily['date']]).count()
    #   
    count_supermarketdf = DataFrame(count_supermarket)
    #
    count_supermarketdf.reset_index(level=0, inplace=True)
    
    count_supermarketdf.set_index(['date']).head()
    
    count_supermarketdf.columns = ['date',supermarket+'s_count']

   
    #OLD
    count_supermarketdf_OLD = pd.read_csv('/home/mint/workinprogress/global/global_code/KPIs/'+supermarket+'/dailycounts.csv')
    count_supermarketdf_OLD.drop_duplicates(cols=None, take_last=False, inplace=True)
    
    
    if not len(count_supermarketdf_OLD[count_supermarketdf_OLD['date'] == datetime.date.strftime(date.today(), '%Y-%m-%d')]) ==0:
        count_supermarketdf_OLD = count_supermarketdf_OLD[count_supermarketdf_OLD['date'] != datetime.date.strftime(date.today(), '%Y-%m-%d')]

    #NEW
    count_supermarketdf_NEW = pd.concat([count_supermarketdf,count_supermarketdf_OLD])
    count_supermarketdf_NEW = count_supermarketdf_NEW[['date',supermarket+'s_count']]
    count_supermarketdf_NEW.to_csv('/home/mint/workinprogress/global/global_code/KPIs/'+supermarket+'/dailycounts.csv')



    # create counts by item name
    item_count_supermarketdf = DataFrame(supermarketDaily.groupby(['ons_item_name'])['std_price'].count())
    item_count_supermarketdf.reset_index(level=0, inplace=True)

    today = datetime.date.strftime(date.today(), '%Y_%m_%d')

    item_count_supermarketdf.columns = ('ONS_ITEM_NAME' , today)
    
    #merge new data onto file
    item_count_supermarketdf_OLD = pd.read_csv('/home/mint/workinprogress/global/global_code/KPIs/'+supermarket+'/'+supermarket+'_item_counts.csv')


    if today in item_count_supermarketdf_OLD.columns:
                
        item_count_supermarketdf_OLD= item_count_supermarketdf_OLD.drop(today, axis = 1)

    item_count_supermarketdf_NEW = pd.merge(item_count_supermarketdf_OLD,item_count_supermarketdf, how='outer', on='ONS_ITEM_NAME')

    
        
    #deal with zero counts
    item_count_supermarketdf_NEW.fillna(0, inplace = True)
    #calculate average and difference today and average

    #Number of columns to divide by
    item_count_supermarketdf_NEW['numcol'] = 0
    item_count_supermarketdf_NEW['numcol7'] = 1
        
           
    for row_index, rows in item_count_supermarketdf_NEW.iterrows():
            
        totcol = item_count_supermarketdf_NEW.shape[1]
            
        for i in range (5,11):
            try:
                if int(item_count_supermarketdf_NEW.ix[row_index,i]) > 0: 
                    item_count_supermarketdf_NEW.ix[row_index,'numcol7'] = item_count_supermarketdf_NEW.ix[row_index,'numcol7'] +1
            except:
                print 'Error at row' , row_index , 'and column' ,i
                
        for i in range(5,totcol-2):
            try:
                if int(item_count_supermarketdf_NEW.ix[row_index,i]) > 0:
                    item_count_supermarketdf_NEW.ix[row_index,'numcol'] = item_count_supermarketdf_NEW.ix[row_index,'numcol'] +1
            except:
                print 'Error at row' , row_index , 'and column' ,i
                       
                    
    #Calculate the average
      
    item_count_supermarketdf_NEW.sort(inplace=True, axis=1, ascending = False)

    #NOTE: ix index will need updating if new columns other than new dates are included in dataframe
    item_count_supermarketdf_NEW['MEAN_COUNT'] = map(int, (item_count_supermarketdf_NEW.ix[:,7:totcol].sum(axis = 1)) /item_count_supermarketdf_NEW['numcol'])
    item_count_supermarketdf_NEW['MEAN_7DAY'] = map(int, (item_count_supermarketdf_NEW.ix[:,7:14].sum(axis = 1))/item_count_supermarketdf_NEW['numcol7'])
        
    item_count_supermarketdf_NEW['Dif:TODAY-MEAN'] = map(int, (item_count_supermarketdf_NEW[today]-item_count_supermarketdf_NEW['MEAN_COUNT']))
    item_count_supermarketdf_NEW['Dif:TODAY-7DAYMEAN'] = map(int, (item_count_supermarketdf_NEW[today]-item_count_supermarketdf_NEW['MEAN_7DAY']))
        
    #sort into descending order to keep most recent date first                                 
    item_count_supermarketdf_NEW.sort(inplace=True, axis=1, ascending = False)
    
    #do not output numcol and numcol7
    item_count_supermarketdf_NEW.ix[:,2:totcol].to_csv('/home/mint/workinprogress/global/global_code/KPIs/'+supermarket+'/'+supermarket+'_item_counts.csv', index = False)




todays_date = datetime.date.strftime(date.today(), '%Y%m%d')


try:
    update_prices_daily_count('sainsbury' , todays_date)

except Exception as e:
    print e

try:
    update_prices_daily_count('tesco' , todays_date)

except Exception as e:
    print e

try:
    update_prices_daily_count('waitrose' , todays_date)

except Exception as e:
    print e
    
