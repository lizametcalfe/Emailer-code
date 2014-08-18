#this is the code to call the other components of Munge; split up by logical function 
# this is the first set of object classes which obtain data from the dictionary and the scraper output 
# then it merges them
# the locations of the dictionary and the scraper output are contained in this module 
import finder 
import manipulation 
#Purpose of code: Process the daily file, back up to the NAS and create a longitudinal data set

import time
import datetime
from datetime import date
from time import strptime

#Input:
#"dates" User to change dates otherwise todaty's date will be used
dates = datetime.date.strftime(date.today(), '%Y%m%d')


# 1. This imports the scraper data 
raw_data_object = finder.Raw_finder('waitrose',dates)
print(raw_data_object)
# this is the supermarket data 
supermarketDF = raw_data_object.supermarket_finder()
#print supermarketDF 

# 2. Manipulation of the Raw_data; initialise the object
manipulation_object = manipulation.Munger('waitrose',supermarketDF)
print(manipulation_object)
# manipulated supermarket data 
supermarketDF = manipulation_object.munge_1()

# 3. Merge with the dictionary; initialise the object
merged_object = finder.Merger('waitrose',supermarketDF,dates)
print(merged_object)

test = merged_object.combine_data()