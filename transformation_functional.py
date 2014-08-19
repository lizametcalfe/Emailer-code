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
from prices_functions import *

import time
import datetime
from datetime import date
from time import strptime

import datetime
from datetime import date

# define the program using object based programming conventions
# firstly define the functions which are going to merge and format the data 
# secondly define the functions that are going to manipulatate and analyse the data 

class string_feeder(object):
    def __init__(self,supermarket,supermarket2):
        self.supermarket = supermarket
        self.supermarket2 = supermarket2 

    def __str__(self):
        printer = "supermarket string feeder object\n"
        printer += "supermarket:\n " + self.supermarket
        return printer 

    def feeder(): 
        supermarket2 = self.supermarket2
        for row_index, row in supermarket2.iterrows():
            
            name = supermarket2.ix[row_index,'product_name'].strip()
                   
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
                supermarket2.ix[row_index, 'brand'] = brands(supermarket2,name)
            
            except Exception as e: 
                print 'error with brand at row:' , row_index, 'name=', name, 'error = ',e
                              
            # Define range type
            try:       
                supermarket2.ix[row_index, 'range'] = range_type(supermarket2,name)    
            
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