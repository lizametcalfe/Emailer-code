# check to identify whether an item is on a multibuy discount 
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

test = pd.read_csv('/home/robert/project_2/supermarket_scraper/output/tesco/tesco_test.csv')
testDF = DataFrame(test)
counter = len(testDF)
print('input data count: ',counter)

testDF['multibuy_ANY'] = testDF['offer'].str.contains("Any")
testDF['multibuy_BUY'] = testDF['offer'].str.contains("Buy")
testDF.to_csv('/home/robert/project_2/supermarket_scraper/output/tesco/tesco_multibuy.csv', index = False)
