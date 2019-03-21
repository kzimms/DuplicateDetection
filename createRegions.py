# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 08:52:15 2019

@author: FG577RC, Kathryn Zimmerman

This script opens all the files that need to be combined, combines them and 
then segments them into new 'region' files based on the country code. This
allows for clustering on records with similar address contructs and languages.
"""

import pandas as pd
import numpy as np

######### ALL CHANGES IN THIS BLOCK ###########################
filePath = "Customer"           # Folder name where files stored
fileList = ["CSV_DCP_RE2_KNA1","CSV_PHI_RE1_KNA1"]   # List of file names without .csv ending that contain the data and need to be combined
###############################################################

def segmentRegion(countries, df):
    segmented = pd.DataFrame(columns=df.columns)
    #segmented.columns = df.columns
    rest = pd.DataFrame(columns=df.columns)
    #rest.columns = df.columns
    for index, row in df.iterrows():
        if row['LAND1'] in countries:
            segmented.append(row)
        else:
            rest.append(row)
    return segmented, rest

def segmentRegionQuicker(countries, df):
    segmented = pd.DataFrame(columns=df.columns)
    #segmented.columns = df.columns
    rest = pd.DataFrame(columns=df.columns)
    #rest.columns = df.columns
    for index, row in df.iterrows():
        if row['LAND1'] in countries:
            segmented.append(row)
        else:
            rest.append(row)
    return segmented, rest

combined = pd.DataFrame()
for i in range(len(fileList)):
    if i == 0:
        combined = pd.read_csv("../"+filePath+"/"+fileList[i]+".csv", dtype='str')
        print combined.head(5)
    else:
        combined = combined.append(pd.read_csv("../"+filePath+"/"+fileList[i]+".csv", dtype='str'))

NAmerica = ['US','CA']
SAmerica = ['AR','AW','BB','BF','BH','BM','BO','BR','BS','BZ','CL','CO','CR', 'DM', 'DO', 'EC', 'GT', 'GY', 'HN', 'JM', 'KY', 'MQ', 'MX', 'NI', 'PA', 'PE', 'PR', 'PY',  'SN', 'SV', 'TT', 'UY', 'VE', 'VG', 'VI']
#Carribean = ['AN','AT','AB','BB','BO','BA', 'CB', 'DR','GR','HA','JM','SK','SL','SV','VI','GL','TT']
Europe = ['AD','AL','AN','AT','AZ','BE','BY','CH','CZ','DE','DK','EE','ES','FI','FR','GB','GI','GR','HR','HU','IE','IL','IS','IT','LI','LT','LU','LV','MC','MD','ME','MK','MT','NL','NO','PL','PT','RO','RS','RU','SE','SI','SK','SZ','TR','UA']
MEAfrica = ['AE','BW','CI','CM','DZ','EG','ET','GH','IQ','JO','KE','KW','LB','LR','LY','MA','ML','MU','MW','MZ','NA','NG','OM','RE','RW','SA','SD','SL','SR','SY','TN','TZ','UG','YE','ZA','ZM','ZW'] 
AsiaPacific = ['AM','AU','BA','BD','BG','CN','CY','FJ','GE','HK','ID','IN','IR','JP','KH','KR','KZ','LK','MH','MM','MY','NC','NP','NZ','PH','PK','QA','SG','TH','TW','UZ','VN']
#Oceania = ['AU','FJ','GM','MA','MI','NB','NC','NZ','PN','PA']

NAmericaData = combined.loc[combined['LAND1'].isin(NAmerica)]
SAmericaData = combined.loc[combined['LAND1'].isin(SAmerica)]
EuropeData = combined.loc[combined['LAND1'].isin(Europe)]
MEAfricaData = combined.loc[combined['LAND1'].isin(MEAfrica)]
AsiaPacificData = combined.loc[combined['LAND1'].isin(AsiaPacific)]

NAmericaData.to_csv("../"+filePath+"/Combined_NAmerica_Test.csv")
SAmericaData.to_csv("../"+filePath+"/Combined_SAmerica.csv")
EuropeData.to_csv("../"+filePath+"/Combined_Europe.csv")
MEAfricaData.to_csv("../"+filePath+"/Combined_MEAfrica.csv")
AsiaPacificData.to_csv("../"+filePath+"/Combined_AsiaPacific.csv")

