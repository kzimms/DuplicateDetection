# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 16:36:42 2019

@author: FG577RC, Kathryn Zimmerman

This script executes a SQL query on a HANA database and pulls in records in
batches of 20,000 and appends each pull to a Pandas DataFrame. 

Once the DataFrame has 300,000 records, it empties the DataFrame by saving it
to a csv file. This step is important for time efficiency.
"""

import pyhdb
import numpy as np

######### ALL CHANGES IN THIS BLOCK ###########################
HANAhost = "XX.XXX.XX.XXX"      # put host number in "quotes"
HANAport = 30115                # keep port number as integer
HANAuser = ""             # put username in "quotes"
HANApassword = ""     # put password in "quotes"
SQLquery = ""         # SQL query that would be used in HANA to access data
masterData = ""         # Folder where the data will be saved
fileName = ""           # base of the file name where pull will be saved
###############################################################
    
connection = pyhdb.connect(
        host= HANAhost,
        port= HANAport,
        user= HANAuser,
        password= HANApassword
        )

cursor = connection.cursor(SQLquery)
cursor.execute()
print 'execute successful'


from pandas import DataFrame
import pandas as pd
row = cursor.fetchmany(20000)
df = pd.DataFrame()

i = 0
while row is not None:
    try:
        newdf = pd.DataFrame(row)
        df = df.append(newdf)
        row = cursor.fetchmany(20000)
    except:
        row = cursor.fetchmany(20000)
        print "in except"
    i += 20000
    print i
    if i % 300000 == 0:
        df.to_csv("../"+masterData+"/"+fileName+"_"+str(i)+".csv", header=False, index=False, encoding='utf-8')
        df = pd.DataFrame()

df.to_csv("../"+masterData+"/"+fileName+"_Full.csv", header=False, index=False, encoding='utf-8')


