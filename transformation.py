# define the program using object based programming conventions
# firstly define the functions which are going to merge and format the data 
# secondly define the functions that are going to manipulatate and analyse the data 
class transform(object):

    def new_match(self,fil,name):   
        """Function to derive a new match score for the item. Based on the 'include' 'exclude and 'remove' columns
        in the dictionary. 
        If the product name includes only includes score  = 1, 
        if it contains an excluded word; score = 0.5, and
        if it contains a word from the remove column the score given is 0.0 """
        # print 'test1', name, 'CRAP'
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
    
    
        if any(p in (fil.ix[row_index,'ons_item_name'].strip().upper()) for p in ('TOMATO', 'POTATO', 'ONION', 'GRAPE', 'BANANA', 'STRAWBERRY')):
            if fil.ix[row_index,'std_unit'].strip() !='kg':
                match = 0.5
    
        return match	

    def category1(self,fil,name):
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

    def multiples(self,fil,name):
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
     

    
    def create_vol(self,fil,name):
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

    def brands(self,name):
          
        Ownbrand = supermarket.strip().upper()
        
        if Ownbrand in name:
            return Ownbrand
        else:
            return name.split()[0]
     
        
    def range_type(self,name):
        
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
        
    
    def extract_AVB(self,fil,name):
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

