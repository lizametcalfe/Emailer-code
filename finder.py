
class finder(object):
	#after self are the attributes 
	def supermarket_finder(self,supermarket,date):
	    #read in file with the_date
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
	        print counter

	    except:
	        print 'No data available for', date
	        counter = 0

	    return supermarketDF

	def dictionary_merger(self,supermarketDF):
		#locate dictionary 
		match_dictionary = DataFrame(data=pd.read_csv('/home/mint/workinprogress/Global_Code/dictionary/match_dictionary.csv'))
		# sort 
		supermarketDF.sort_index(inplace=True, axis = 0, by=['ons_item_name','std_price'])
        # merge 
        supermarket2=pd.merge(supermarketDF,match_dictionary, how='inner', on='ons_item_name', left_index = False, right_index=False)
        
        return supermarket2 