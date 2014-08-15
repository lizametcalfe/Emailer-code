#Changes made:

#1. location name changed in following line:
#"oldfile.to_csv('/nas/projects/ProjectT004/Prices/Data/' + supermarket + '_longitudinal_backup.csv', index = False)"
#"Prices" removed as points to non-existent locaiton

#2. Sainsbury's files were being saved to tesco folder

#Purpose of code: Process the daily file, back up to the NAS and create a longitudinal data set

import datetime
from datetime import date
#Input:
#"dates" User to change dates otherwise todaty's date will be used
dates = datetime.date.strftime(date.today(), '%Y%m%d')
#dates = '20140715'


#Output:
#


#Author: Leone Wardman  - oh no - delete delete delete HAHAHA!!!
#Edited by RB 

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


# The code is written in a functional format; first job is to parametise the functions 
def  daily_munge(supermarket, date) :  

    def new_match(fil,name):   
        """Function to derive a new match score for the item. Based on the 'include' 'exclude and 'remove' columns
        in the dictionary. 
        If the product name includes only includes score  = 1, 
        if it contains an excluded word; score = 0.5, and
        if it contains a word from the remove column the score given is 0.0 """

        includes = [i.strip() for i in fil.ix[row_index,'include'].split(' ') if i.strip()]
        excludes = [e.strip() for e in fil.ix[row_index,'exclude'].split(' ') if e.strip()]
        removes = [r.strip() for r in fil.ix[row_index,'remove'].split(' ') if r.strip()]
    	
           
        # For each new record set match to 0.0    
        match = 0.0
    
        # Allocate a value, if any of the items in the list matches the scrore is 1.0, 0.5, 0.0 respectively 
        if  'NONE' in includes: 
            match = 1.0
    
        else :
            for include in includes:
                if include in name:
                    match = 1.0;
                
        if (not 'NONE' in excludes): 
            for exclude in excludes:
                if exclude in name:
                    if not (exclude == 'SPREAD' and 'SPREADABLE' in name):
                        match = 0.5
                
        if (not 'NONE' in removes):
            for remove in removes:
                if remove in name:
                    match = 0.0
    
    
        if any(p in (supermarket2.ix[row_index,'ons_item_name'].strip().upper()) for p in ('TOMATO', 'POTATO', 'ONION', 'GRAPE', 'BANANA', 'STRAWBERRY')):
            if supermarket2.ix[row_index,'std_unit'].strip() !='kg':
                match = 0.5
    
        return match


    def category1(fil,name):
        """ Function to set the sub_index for the product, based
            on the criteria in 'categoryt1' from the dictionary """
          
        count = 0
        
        for s in (fil.ix[row_index, 'category1'].split()):
            
            if s == 'NONE':
                return s
            
            elif s in name: 
                count = count+1
                if any(cola in s for cola in ('COKE', 'COCA', 'COCO')):
                    cat1 = 'COKE'
                elif count > 1:
                    cat1= 'MIXED'
                else:
                    cat1=  s
                    
        if count >= 1:
            return cat1
        
        else:  
            return 'OTHER'
 
    
    
    def multiples(fil,name):
        """ A function to create an indicator with the number of items included in the product,
        for example, 4X350ML would return '4'. If there are not more than 1, or the number
        is not specified, multipack will = 1 """
        
        # Because tea bags don't usually follow the X format at tesco
        if any(s in supermarket for s in('tesco', 'waitrose')) and 'TEA' in fil.ix[row_index, 'ons_item_name'].strip().upper():
            
            if '1706' in name:

                atpos = re.search("TEA", name)
                return filter(lambda x: x.isdigit(), name[atpos.start()-4:atpos.start()].strip())
                
            else:

                atpos = re.search("\d", name)
                return filter(lambda x: x.isdigit(), name[atpos.start():atpos.start()+3].strip())     
    
        else:
        
        # Search for a volume pattern in the data
        
            Xpos = re.search("[\d][X][\s\d]", name) # 12X350ML or 12X 350ML
                    
            if Xpos == None:
            
                Xpos = re.search("[\d][\s][X]", name) # 12 X350ML or 12 X 350ML 
            
                if Xpos == None:
                
                    Xpos = re.search("[X][\d]", name) # X5 
                
                    if Xpos == None:
                    
                        Xpos = re.search("[X][\s][\d]", name) # X 5 
                    
                        if Xpos == None and supermarket == 'waitrose':
                            
                            Xpos = re.search("[\s\d][\d][S]", name) # 24S 4S (Waitrose )
                    
            if Xpos != None:  
                
                if name[Xpos.start()].isdigit():
                    
                    return filter(lambda x: x.isdigit(),  name[Xpos.start()-1:Xpos.start()+2] )
                
                else: return filter(lambda x: x.isdigit(), name[Xpos.start()+1:Xpos.start()+4] )  # take numbers to right of X
        
            else:
                return 1
     

    
    def create_vol(fil,name):
        """This function id for extracting volume information from the product.
	Note that this is the total volume of all items if there are multiples. For e.g. if there aer 4X375ML
	the volume will be 1500. The volumes have been standardised to GRAMS and ML, and have a value of '-1'
	if there is no relevant volume information"""

        search =  fil.ix[row_index,'std_unit'].strip()

        Z = ""
        VOL = ""
        atpos = -1

        # Find type of unit
        if search == 'kg':
            atpos = name.rfind('KG')
            if atpos > 1:
                unit = 'KG'
            
            else:
                atpos = name.rfind('G')
                if atpos > 1:
                    unit = 'G'
                
                else:
                    unit = 'NONE'
                
        elif search == 'l':
            atpos = name.rfind('ML')

            if atpos > 1:
                unit = 'ML'

            else:
                atpos = name.rfind('CL')
                if atpos > 1 and ( name[atpos-2:atpos-1].isdigit() or any(s in name[atpos-2:atpos-1] for s in ("X", ".")) ):
                    unit = 'CL'
                    
                else:
                    atpos = name.rfind('L')
                    if atpos > 1:
                        unit = 'L'
                    
                    else:
                        unit = 'NONE'


        elif search == 'each' or search == 'unknown':
            unit  = 'NONE'


        if (not atpos > 1) or (unit == 'NONE'):
            VOL = -1

        else: #deal with real units

            Voltype = 'num'

            #Decimals
            VolStr = (name[atpos-5:atpos].strip())
            DecPos = VolStr.rfind('.')

            if DecPos >= 1 and VolStr.strip()[DecPos-2:DecPos-1].isdigit():
                VolStr = VolStr[DecPos-2:]
                Voltype = 'dec'


            elif DecPos >= 1 and VolStr.strip()[DecPos-2:DecPos-1].isdigit():
                VolStr = VolStr[DecPos-1:]
                Voltype = 'dec'


            # Multiples e.g 4X350ML
            elif 'X' in name[atpos-4:atpos]:
                VolStr = name[atpos-4:atpos].strip()[((name[atpos-3:atpos].find('X'))+1):]


            elif '%' in name[atpos-4:atpos]:
                VolStr = name[atpos-4:atpos].strip()[((name[atpos-3:atpos].find('%'))+1):]


            # Regular patterns
            else:
                VolStr = name[atpos-4:atpos].strip()


            if Voltype  == 'dec':
                if unit == 'L' or unit == 'KG':
                    VOL = int(float(VolStr)*1000)

                elif unit == 'CL' or unit== 'ML':
                    VOL = int(float(VolStr)*10)

                else: VOL = -1

            else:
                Z = filter(lambda x: x.isdigit(),  VolStr )

                if unit == 'L' or unit== 'KG':

                    if len(Z)==1:
                        try:
                            VOL = int(Z)*1000
                        except:
                            VOL = -1

                    elif len(Z)==2:
                        try:
                            VOL = int(Z)*100
                        except:
                            VOL = -1

                    elif len(Z)==3:
                        try:
                            VOL =int(Z)*10
                        except:
                            VOL = -1

                    else: VOL = -1


                elif unit =='CL':
                    try:
                        VOL = int(Z)*10
                    except:
                        VOL = -1

                elif unit =='G' or unit =='ML':
                    try:
                        VOL = int(Z)
                    except:
                        VOL = -1

        if VOL ==-1 or ('TEA' in name): 
            return VOL
        
        else:
            return int(VOL)*int(fil.ix[row_index, 'num_units']) 

    def brands(name):
          
        Ownbrand = supermarket.strip().upper()
        
        if Ownbrand in name:
            return Ownbrand
        else:
            return name.split()[0]
     
        
    def range_type(name):
        
        if any(s in name for s in ("PREMIUM", "FINEST", "TASTE THE DIFFERENCE", "DUCHY", "HESTON", "WAITROSE SERIOUSLY")):
            return 'PREMIUM'
              
        elif any(s in name for s in ('BASIC', 'VALUE', 'ESSENTIAL', 'EVERYDAY', 'DISCOUNT')):
            return 'BUDGET'
        
        elif 'ORGANIC' in name:
            return 'ORGANIC'
        
        elif 'FAIRTRADE' in name:
            return 'FAIRTRADE'
        
        else:
            return 'STANDARD'
        
    
    def extract_AVB(fil,name):
        """Function to extract the alcohol volume where applicable. Contains % or -1 if not valid"""
        
        if any(s in  (fil.ix[row_index, 'ons_item_name'].strip().upper()) for s in ("BITTER" , "LAGER", "CIDER", "WINE")):
            startpos = name.find("(")
            stoppos = name.find("%")
           
            if stoppos > 1:
                
                if startpos > 1:
                    AVBStr = float(name[startpos+1:stoppos].strip())
                
                elif name[stoppos-2].strip() == ".":
                    AVBStr = float(name[stoppos-3:stoppos].strip())
                
                else:
                    AVBStr = float(name[stoppos-1:stoppos].strip())
                
                
            else: AVBStr = '-1'
        
        else: AVBStr = '-1'

        return AVBStr    

     
        
    ######## START MUNGE #####

    '''

    Step One: Read in the latest data and apply reformatting as required

    '''
    
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
        
        

    if counter > 0: 
        
        #back up data file to NAS LONG TERM BACK UP
        #/nas/projects/ProjectT004/V2_supermarket_scraper/supermarket_scraper/output/
        try:
            supermarketDF.to_csv('/home/mint/longditudal/output/'+ supermarket + '/'+ file, index = False)
        
        except:
            print 'unable to back up data file for ', supermarket
            
            
        # Data fixes to apply to every file
        for row_index, rows in supermarketDF.iterrows():
            
            
            if supermarket == 'sainsbury':
                
                
                # separate Bananas and grapes from the banana category
                if 'Banana' in supermarketDF.ix[row_index,'ons_item_name'].strip():
                    if 'GRAPE' in supermarketDF.ix[row_index,'product_name'].strip():
                        supermarketDF.ix[row_index,'ons_item_name'] = 'Grapes, per kg'
                        supermarketDF.ix[row_index,'ons_item_no'] = '212722'
                        
                # separate otyher fruit juices from the orange category
                if 'Tropicana' in supermarketDF.ix[row_index,'ons_item_name'].strip():
                    if not 'ORANGE' in supermarketDF.ix[row_index,'product_name'].strip():
                        supermarketDF.ix[row_index,'ons_item_name'] = 'Fruit Juice, not orange, eg. apple'
                        supermarketDF.ix[row_index,'ons_item_no'] = '212006'
                                
                            
            if supermarket == 'tesco':
                
                # separate Fromage Frais and Yoghurts from the banana category
                if 'Yoghurt' in supermarketDF.ix[row_index,'ons_item_name'].strip():
                    if 'FROMAGE FRAIS' in supermarketDF.ix[row_index,'product_name'].strip():
                        supermarketDF.ix[row_index,'ons_item_name'] = 'Yoghurt/Fromage Frais'
                        supermarketDF.ix[row_index,'ons_item_no'] = '211807'
 
            if supermarket == 'waitrose':
          
                # remove healthy cereals from sugar category
                if 'Cereal 1' in supermarketDF.ix[row_index,'ons_item_name'].strip():
                    if not (any(p in supermarketDF.ix[row_index,'product_name'].strip() for p in ('SUGAR', 'FROST', 'CHOC', 'HONEY', 'MAPLE', 'COOKIE', 'CHEER','COCO', 'CARAMEL', 'FROOT', 'GOLD', 'CURIOUS')) ):
                        supermarketDF.ix[row_index,'ons_item_name'] = 'Breakfast Cereal 2, NOT sugar/chocolate coated'
                        supermarketDF.ix[row_index,'ons_item_no'] = '210214'
                         
       
            # separate skim milk from whole milk             
            if supermarketDF.ix[row_index,'ons_item_name'] == 'Shop Milk, whole milk' and any(s in supermarketDF.ix[row_index,'product_name'].strip() for s in ("SKIMMED", "1%")):
                supermarketDF.ix[row_index,'ons_item_name'] = 'Shop Milk,semi-skimmed, per 2 pints/1.136 litre' 
                supermarketDF.ix[row_index,'ons_item_no'] = '211710'
                                    
                                    
            # remove white space from ons_item_name, all supermarkets
            if 'Potato' in supermarketDF.ix[row_index,'ons_item_name'].strip():
                supermarketDF.ix[row_index,'ons_item_name'] = supermarketDF.ix[row_index,'ons_item_name'].strip()
                
                if (not supermarket  == 'waitrose') and any(p in supermarketDF.ix[row_index,'product_name'].strip() for p in ('NEW', 'MINI', 'SMALL')):
                    supermarketDF.ix[row_index,'ons_item_name'] = 'Potatoes, new'
                    supermarketDF.ix[row_index,'ons_item_no'] = '212399'
                    
                elif 'BAKING' in supermarketDF.ix[row_index,'product_name'].strip():
                    supermarketDF.ix[row_index,'ons_item_name'] = 'Potatoes, baking'
                    supermarketDF.ix[row_index,'ons_item_no'] = '212361'
          
                    
                    
        
        ''' 
            Step Two: attach the dictionary for processing the data and apply the indicator functions 
        '''
        
        #read match_dictionary file
        #/home/projectt004/Prices/KPIs
        match_dictionary = DataFrame(data=pd.read_csv('/home/mint/workinprogress/Global_Code/dictionary/match_dictionary.csv'))
    	# print 'rb test 2', type(match_dictionary), match_dictionary                                    
        #merge the files
        supermarketDF.sort_index(inplace=True, axis = 0, by=['ons_item_name','std_price'])
        supermarket2=pd.merge(supermarketDF,match_dictionary, how='inner', on='ons_item_name', left_index = False, right_index=False)
        
        # set date column
        supermarket2['date'] =  date[:4]+'_'+date[4:6]+'_'+date[6:] 
        #print supermarket2 temp file
        supermarket2.to_csv('/home/mint/longditudal/output/merged_file.csv', index = False)
        # test some manual adjustments
        supermarket2 = DataFrame(data=pd.read_csv('/home/mint/longditudal/output/merged_file.csv'))
        
        # NOW APPLY THE FUNCTIONS TO THE DATA    
        
        for row_index, row in supermarket2.iterrows():
            
            name = supermarket2.ix[row_index,'product_name'].strip()
            #print 'RB test',name
     
            
            # Write the match score to the record  
            try:           
                supermarket2.ix[row_index,'new_match'] = new_match(supermarket2,name)
            
            except Exception as e: 
                print 'New_match error in row:', row_index, 'name=', name, 'include=', includes, 'error = ',e
            
            

            # derive multiples
            try:  
                supermarket2.ix[row_index,'num_units'] = multiples(supermarket2,name)
            
            except Exception as e: 
                print 'error with multipack, row =' ,row_index, 'name=', name,  row_index, 'error = ',e
       
            
            # create total volume in ML/GRAMS
            try:    
                supermarket2.ix[row_index,'volume_total']=create_vol(supermarket2,name)
            
            except Exception as e:
                print 'volume error line=', row_index, 'name=', name, #'unit = ', unit, 'Voltype = ', Voltype
                print 'error = ',e 
            

            # Add on subcategories
            try:     
                supermarket2.ix[row_index, 'sub_type'] = category1(supermarket2,name)
            
            except Exception as e: 
                print 'error with sub_type, row = ' , row_index, 'name =' , name, 'error = ',e
            
            
            # Define brand type
            try:    
                supermarket2.ix[row_index, 'brand'] = brands(name)
            
            except Exception as e: 
                print 'error with brand at row:' , row_index, 'name=', name, 'error = ',e
                    
                    
            # Define range type
            try:       
                supermarket2.ix[row_index, 'range'] = range_type(name)    
            
            except Exception as e: 
                print 'error with range at row:' , row_index, 'name=', name,'error = ',e
                            
            
            # Extract alcohol volume
            try:    
                supermarket2.ix[row_index, 'alcohol_volume'] = extract_AVB(supermarket2,name)
            
            except Exception as e: 
                print 'error in alcohol volume row =' , row_index, 'name=', name, 'error = ', e
          
          
            # To view a product uncomment this section and update product name
            
            #if supermarket2.ix[row_index,'ons_item_name']=='Tea bags, per packet of 80, 250g' and supermarket2.ix[row_index,'new_match']==0.0:
                #print 'match', supermarket2.ix[row_index,'new_match'], 'sub_type=' ,supermarket2.ix[row_index, 'sub_type'],        'brand=', supermarket2.ix[row_index,'brand'] ,          'range=', supermarket2.ix[row_index,'range'] ,           'num_units=', supermarket2.ix[row_index,'num_units'] ,         'VOL=', supermarket2.ix[row_index,'volume'] ,            'AVB=', supermarket2.ix[row_index,'alcohol_volume'] ,         'product' , supermarket2.ix[row_index,'product_name']
        
        
        print 'Processed'
      
        
        
       
        '''
       
        Step Three: Append date to longitudinal file and write out to csv

        '''

              
        # read in yesterdays data set and check to make sure that there is not data for todays date in the file. 
        # If not then append todays date to the old file
        # CHECK YESTERDAYS FILE 
       
        file = '/home/mint/longditudal/output/' + supermarket + '_longitudinal.csv'

        try:
            oldfile = pd.read_csv(file)
            
            L = len(oldfile)
            
            
            if L > 0: 
            	print "L equals ", L
                
                #Make a back up of today's file to NAS before appending new data
                oldfile.to_csv('/home/mint/longditudal/output/' + supermarket + '_longitudinal_backup.csv', index = False)
                
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
           
        newfile2.to_csv(file, index = False)
        
        print 'newfile=', newfile2.shape
            
	
            
# CALL DAILY_MUNGE #########################################################################    


''''dates =['20140414','20140415','20140416','20140417','20140418','20140419','20140420','20140421','20140422','20140423','20140424','20140425','20140426','20140427','20140428','20140429',
       '20140430','20140501','20140502','20140503','20140504','20140505','20140506','20140507','20140508','20140509','20140510','20140511','20140512','20140513','20140514','20140515',
       '20140516','20140517','20140518','20140519','20140520','20140521','20140522','20140523','20140524','20140525','20140526','20140527','20140528','20140529','20140530','20140531',
       '20140601','20140602','20140603','20140604','20140605','20140606','20140607','20140608','20140609','20140610','20140611','20140612','20140613','20140614','20140615','20140616',
       '20140617','20140618','20140619','20140620','20140621','20140622','20140623','20140624','20140625','20140626','20140627','20140628','20140629','20140630','20140701','20140702'
        '20140703','20140704','20140706','20140705', '20140707']

for dates in dates:'''

daily_munge(supermarket='waitrose', date='20140812')
#daily_munge(supermarket='tesco', date=dates)
#daily_munge(supermarket='sainsbury', date=dates)
