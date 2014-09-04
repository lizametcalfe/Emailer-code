
import pandas as pd
import numpy as np
import matplotlib as mat
import matplotlib.pyplot as plt
import datetime
import csv
import os
import fnmatch
import re

from pandas import groupby
from pandas import DataFrame
from pandas import Series

import time
import datetime
from datetime import date
from time import strptime

import datetime
from datetime import date

class Raw_finder(object):
	#after self are the attributes 

	def __init__(self,supermarket,date,scraper_output,dictionary):
		self.supermarket = supermarket
		self.date = date
		self.scraper_output = scraper_output
		self.dictionary = dictionary 

	def __str__(self):
		printer = "supermarket object\n"
		printer += "supermarket:\n " + self.supermarket + "\n" + "date:\n " + self.date
		return printer 

	def supermarket_finder(self):
	    #read in file with the_date
	    # attributes 
	    supermarket = self.supermarket
	    date = self.date 
	    scraper_output = self.scraper_output
	    filename = str(supermarket)+str('_products_')+str(date)+str('*')
	    print filename
	    counter = 0
	    for file in os.listdir(scraper_output + supermarket+'/'):
	    
	        if fnmatch.fnmatch(file, filename):
	              
	            atpos = file.find('_2')
	            stopos = file.find('.')
	            time = file[atpos+1:stopos]
	        
	            if counter == 0:
	                file2 = scraper_output + supermarket+ '/'+ file
	                time_before = file[atpos+1:stopos]
	                print "file equals ", file2
	                
	            elif int(time) > int(time_before):
	                file2 = scraper_output + supermarket + '/'+ file
	                time_before = file[atpos+1:stopos]
	                print "file equals ", file2
	            
	            counter = counter+1

	    try:
	        supermarketDF = DataFrame(data=pd.read_csv(file2))
	        #supermarketDF.drop_duplicates(cols=None, take_last=False, inplace=True)
	        return supermarketDF
	        

	    except:
	        print 'No data available for', date
	        counter = 0

class Merger(object):

	def __init__(self, supermarket, supermarketDF,date,dictionary):
		self.supermarket = supermarket
		self.supermarketDF = supermarketDF 
		self.date = date 
		self.dictionary = dictionary 

	def __str__(self):
		counter =  len(self.supermarketDF)
		printer = "supermarket dictionary merge object\n"
		printer += "supermarket:\n " + self.supermarket + "\n" + "merge the dicitonary and the data:\n "  
		#print ("elephant",counter)
		return printer 

	def combine_data(self):
		dictionary = self.dictionary
		match_dictionary = pd.read_csv(dictionary + '/dictionary.csv')
		match_dictionary = DataFrame(match_dictionary)
		match_dictionary['ons_item_name'] = match_dictionary['ons_item_name'].map(lambda x: x.strip())
		#counter = len(match_dictionary)
		#print('dictionary size: ',counter)
		supermarket = self.supermarket
		supermarketDF = self.supermarketDF
		supermarketDF['ons_item_name'] = supermarketDF['ons_item_name'].map(lambda x: x.strip())
		supermarketDF.sort_index(inplace=True, axis = 0, by=['ons_item_name','std_price'])
		supermarket2=pd.merge(supermarketDF,match_dictionary, how='inner', on='ons_item_name', left_index = False, right_index=False)
		# set date column
		date = self.date
		supermarket2['date'] =  date[:4]+'_'+date[4:6]+'_'+date[6:] 
		#supermarket2.to_csv('/home/mint/longditudal/output/merged_file_missing_items.csv', index = False)
		#counter = len(supermarket2)
		#print('merged counter: ', counter)
		return supermarket2
		
			
class Longterm(object):
	
	def __init__(self,supermarket,supermarket2,long_term_store):	
		self.supermarket = supermarket
		self.supermarket2 = supermarket2
		self.fil = long_term_store

	def __str__(self):
		#counter =  len(self.supermarketDF)
		printer = "supermarket long term series object\n"
		printer += "supermarket:\n " + self.supermarket + "\n" + "backup to longterm storage:\n " 
		return printer

	def long_series(self):
		supermarket = self.supermarket
		fil = self.fil
		supermarket2 = self.supermarket2
		counter = len(supermarket2)
		print('read in file for long term storage:',  counter)
	'''
        try:
            oldfile = pd.read_csv(fil+ supermarket + '/_longitudinal.csv')
            
            L = len(oldfile)
            
            if L > 0: 
            	print "L equals ", L
                
                #Make a back up of today's file to NAS before appending new data
                oldfile.to_csv(fil + supermarket + '/_longitudinal_backup.csv', index = False)
                
                print 'oldfile = ', len(oldfile)
               
                #Check to make sure that the new data is not already in the file, for e.g. if rerunning code
                if  not (len(oldfile[oldfile['date'] == date[:4]+'_'+date[4:6]+'_'+date[6:]]) == 0 ):
                    print 'duplicate date'
                    # deletes current version of date from the file
                    oldfile = oldfile[oldfile['date'] != date[:4]+'_'+date[4:6]+'_'+date[6:]]
                    
                newfile = oldfile.append(supermarket2, ignore_index = True)
                    
                newfile.sort(columns=('ons_item_name','product_name', 'date') ,axis = 0, ascending = True, inplace = True)
                         
        except:        
            newfile = supermarket2
            print "L less than 1"
            
        # Write out new data set
       
        cols = ['date', 'store', 'ons_item_no', 'ons_item_name',  'product_name', 'new_match', 
                'item_price_num', 'unit_price', 'units', 'std_price', 'std_unit',  'volume_total',    
                'num_units', 'sub_type', 'brand', 'range', 'alcohol_volume', 'timestamp', 'product_type', 'promo', 'offer']
       
            
        newfile2 = newfile.ix[:, cols]
           
        newfile2.to_csv(fil+ supermarket +'/_longitudinal.csv', index = False)
        
        print 'newfile=', newfile2.shape
    '''