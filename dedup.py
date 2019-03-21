# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 12:16:29 2019

@author: FG577RC, Kathryn Zimmerman

This script takes in a combined regional csv file and saves two files in the same
folder. It pre-processes the data and then performs clustering at different 
levels of granularity. The returned files contain cluster numbers. The first is
only records for which duplicates have been identified, the second contains all
records with non-duplicate records given a cluster number of 0.
"""

import prepare, DBSCAN
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

######### ALL CHANGES IN THIS BLOCK ###########################
filePath = "Vendor"           # Folder name where files stored
region = "NAmerica"             # Region from files created in createRegions.
num_features = 500000           # max number of features to be created during TF-IDF. If this gets maxed out, increase it.
epsilons = [0.05, 0.12,0.15]     # list of different levels of granularity for duplicates to be found. Lower the epsilon, the more similar returned results will be.
###############################################################


#df = pd.read_csv("../"+filePath+"/Combined_"+region+"_Test.csv", dtype='str', keep_default_na=False)
df = pd.read_csv("../"+filePath+"/Test2.csv", dtype='str', keep_default_na=False)
print(df.head(5))

data = df.to_numpy()

processedData = prepare.preprocess(data)

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

# data is highly unique, changing max_df is not necessary.
tfidf_vectorizer = TfidfVectorizer(max_df = .3, min_df=2, stop_words='english',
                        max_features=num_features, use_idf=True, ngram_range=(1,1))

#fit the vectorizer to data
tfidf_matrix = tfidf_vectorizer.fit_transform(processedData)
print "TF-IDF shape: ", tfidf_matrix.shape
num_records, num_features = tfidf_matrix.shape

# DBSCAN
from sklearn.metrics.pairwise import cosine_similarity

# Create RecordID, cluster #, group # csv
for eps in epsilons:
    clusters = DBSCAN.DBSCAN(tfidf_matrix, eps) #recID to cluster#
    df.insert(0,'Eps: '+str(eps),clusters)

dfnew = df.loc[df['Eps: '+str(epsilons[-1])] != 0]

df.to_csv("../"+filePath+"/"+region+"_Mapping"+ str(num_features)+"_features.csv", sep=',', index=False)
dfnew.to_csv("../"+filePath+"/"+region+"_ClustersOnly_Mapping.csv", sep=',',index=False)
print "Clustering Complete"




