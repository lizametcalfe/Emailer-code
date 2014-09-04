#this is the code to call the other components of Munge; split up by logical function 
# this is the first set of object classes which obtain data from the dictionary and the scraper output 
# then it merges them
# the locations of the dictionary and the scraper output are contained in this module 
import finder 
import manipulation 
import transformation_functional
#Purpose of code: Process the daily file, back up to the NAS and create a longitudinal data set

import time
import datetime
from datetime import date
from time import strptime

def caller(supermarket,dates,long_term_store,scraper_output,dictionary):
	# 1. This imports the scraper data 
	raw_data_object = finder.Raw_finder(supermarket,dates,scraper_output,dictionary)
	print(raw_data_object)
	# this is the supermarket data 
	supermarketDF = raw_data_object.supermarket_finder()
	counter =  len(supermarketDF)
	supermarketDF.to_csv(long_term_store+supermarket+'/test_read_1.csv', index = False)
	print("raw count: ", counter)

	# 2. Manipulation of the Raw_data; initialise the object
	manipulation_object = manipulation.Munger(supermarket,supermarketDF)
	print(manipulation_object)
	# manipulated supermarket data 
	supermarketDF = manipulation_object.munge_1()
	counter =  len(supermarketDF)
	print("count after manipulation:" ,counter)
	supermarketDF.to_csv(long_term_store+supermarket+'/test_read_2.csv', index = False)

	# 3. Merge with the dictionary; initialise the object
	merged_object = finder.Merger(supermarket,supermarketDF,dates,dictionary)
	print(merged_object)
	# Dictionary and supermarket data merged 
	supermarket2 = merged_object.combine_data()
	counter = len(supermarket2)
	print ('Processed: final count after merging: ', counter) 
	supermarket2.to_csv(long_term_store+supermarket+'/test_read_3.csv', index = False)

	# 4. Apply the functions; to create new variables 
	New_variables_object = transformation_functional.string_feeder(supermarket,supermarket2)
	print(New_variables_object)
	# data set with new variables derived from the string 
	final = New_variables_object.feeder()
	counter = len(final)
	print ('Processed: final count after creating new variables: ', counter) 
	final.to_csv(long_term_store+supermarket+'/test_read_4.csv', index = False)

	# 5. longterm storage 
	supermarket2 = final 
	longterm_storage_object = finder.Longterm(supermarket,supermarket2,long_term_store)
	print(longterm_storage_object)
	backup = longterm_storage_object.long_series()


#"dates" User to change dates otherwise todaty's date will be used
dates = datetime.date.strftime(date.today(), '%Y%m%d')
#long term storage, such as the NAS
long_term_store = '/home/dark/work/longterm/'
#direct output from the scrapers 
scraper_output = '/home/dark/work/project_3/supermarket_scraper/output/'
#dictionary 
dictionary = '/home/dark/work/project_1/global_code/dictionary'

caller('waitrose', dates,long_term_store,scraper_output,dictionary)
#caller('tesco', dates,long_term_store,scraper_output,dictionary)
#caller('sainsbury', dates,long_term_store,scraper_output,dictionary)