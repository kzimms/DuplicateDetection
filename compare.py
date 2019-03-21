# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:16:38 2019

@author: FG577RC, Kathryn Zimmerman

This script reads in the SAP grouping file, the just clusters file and the full
clusters file.  
"""

import pandas as pd
import numpy as np
import clusterVerification

######### ALL CHANGES IN THIS BLOCK ###########################
filePath = "" # folder where comparison file will be saved
SAPfilepath = "../.csv" # relative file pathe where SAP genereted matched records are saved
clusterFilepath = "../.csv" # relative filepath where the abbreviated clustered file is saved
fullFilepath = "../.csv" # relative filepath where full clustered file is saved
clusterColumn = "" # col name in the cluster file which contains desired clusters for comparison
recIDColumn = "" # col name in the cluster file which contains unique recordID
SAPrecIDColumn = "" #col name in SAP file which contains the recordID numbers
SAPgroupColumn = "" # col name in SAP file which contains desired group numbers for comparison
###############################################################

misMatch = clusterVerification.verify2(fullFilepath,clusterFilepath,
                        SAPfilepath,clusterColumn,recIDColumn,SAPrecIDColumn,SAPgroupColumn)

misMatch.to_csv("../"+filePath+"/Mismatch_Clusters.csv")
