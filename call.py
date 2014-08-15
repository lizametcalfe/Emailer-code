
class finder(object):
	def locater(supermarket,date):
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
