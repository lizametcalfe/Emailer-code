#this is the code to call the other components of Munge; split up by logical function 
# this is the first set of object classes which obtain data from the dictionary and the scraper output 
# then it merges them
# the locations of the dictionary and the scraper output are contained in this module 
import finder 
#Purpose of code: Process the daily file, back up to the NAS and create a longitudinal data set

import time
import datetime
from datetime import date
from time import strptime

#Input:
#"dates" User to change dates otherwise todaty's date will be used
dates = datetime.date.strftime(date.today(), '%Y%m%d')


# 1. This imports the scraper data 
Waitrose_raw = finder.Raw_finder('waitrose',dates)
print(Waitrose_raw)
# this is a supermarket object, we are now applying the method, to call the correct file by date
# and supermarket 
supermarketDF = Waitrose_raw.supermarket_finder()

# 2. Manipulation of the Raw_data 
