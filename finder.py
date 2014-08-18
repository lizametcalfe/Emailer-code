
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

	def __init__(self,supermarket,date):
		self.supermarket = supermarket
		self.date = date 

	def __str__(self):
		printer = "supermarket object\n"
		printer += "supermarket:\n " + self.supermarket + "\n" + "date:\n " + self.date
		return printer 

	def supermarket_finder(self):
	    #read in file with the_date
	    # attributes 
	    supermarket = self.supermarket
	    date = self.date 
	    filename = str(supermarket)+str('_products_')+str(date)+str('*')
	    print filename
	    counter = 0
	    for file in os.listdir('/home/mint/workinprogress/supermarket_scraper/output/'+supermarket+'/'):
	    
	        if fnmatch.fnmatch(file, filename):
	              
	            atpos = file.find('_2')
	            stopos = file.find('.')
	            time = file[atpos+1:stopos]
	        
	            if counter == 0:
	                file2 = '/home/mint/workinprogress/supermarket_scraper/output/'+ supermarket + '/'+ file
	                time_before = file[atpos+1:stopos]
	                print "file equals ", file2
	                
	            elif int(time) > int(time_before):
	                file2 = '/home/mint/workinprogress/supermarket_scraper/output/'+ supermarket + '/'+ file
	                time_before = file[atpos+1:stopos]
	                print "file equals ", file2
	            
	            counter = counter+1

	    try:
	        supermarketDF = DataFrame(data=pd.read_csv(file2))
	        #supermarketDF.drop_duplicates(cols=None, take_last=False, inplace=True)
	        counter =  len(supermarketDF)
	        supermarketDF.to_csv('/home/mint/longditudal/output/test_read.csv', index = False)
	        return supermarketDF
	        print counter

	    except:
	        print 'No data available for', date
	        counter = 0
