

class manipulation(object):

    def all_super(self,supermarket,fil):
        
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
        
        return supermarketDF
