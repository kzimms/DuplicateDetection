# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 15:45:18 2019

@author: FG577RC, Kathryn Zimmerman

This file creates training and test data for record linkage ML model.
It uses DBSCAN to block or index records and then creates feature vectors for
classifying records within blocks as matches.

"""
import numpy as np
import pandas as pd
import matplotlib
import sklearn

import prepare, DBSCAN, params, featureFuncs

# load data
"""
inputs:
    [df] : nxm dimensional pandas dataframe
    [col]: column name in df which specifies where the data starts
    [max_df] : max proportion of records a word can appear in and be included
    [min_df] : min number of records a word can appear in and be included
    [max_feat] : maximum number of features to be vectorized
    [n_gram] : 
This function combines all columns including and after col and then 
computes TF-IDF on it
returns: a TF-IDF representation of the data after col in df
"""
def makeTFIDF(df, col, max_df=0.3, min_df=2,max_feat=100000, n_gram=1):
    df2 = df.loc[:,col:]
    df2 = df2.to_numpy()
    df3 = prepare.preprocess(df2)
    
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import TfidfVectorizer


    tfidf_vectorizer = TfidfVectorizer(max_df =max_df, min_df=min_df, 
                            stop_words='english', max_features=max_feat, 
                            use_idf=True, ngram_range=(n_gram,n_gram))

    return tfidf_vectorizer.fit_transform(df3)

"""
inputs:
    [tfidf] : NxM tfidf matrix representing data containing duplicates
    [epsilon] : float between 0 and 1 represeting how similar the indexing
        groups will be. The larger the epsilon the larger and less homogenous
        each index will be
returns:
    A matrix of indexing groups and associated full data set
"""
def index(df, tfidf, epsilon):
    clusters = DBSCAN.DBSCAN(tfidf, epsilon)
    df.insert(0,'Eps: '+str(epsilon),clusters)
    return df

"""
inputs: 
    [df] : pd dataframe of records
returns:
    A feature matrix where each row corresponds to a pair of records from df, 
    the last column contains labels
"""
def createPairs(df, tfidf):
    # have to add the labels
    row, col = df.shape
    FEATURES = featureFuncs.getFeatures()
    df = pd.DataFrame(columns=FEATURES)
    for i in range(row):
        for j in range(row):
            if i != j:
                #extract both rows
                row_i = df.iloc[[i]]
                row_j = df.iloc[[j]]
                df.append(featureFuncs.makeFeatures(row_i,row_j, tfidf[i,:], tfidf[j,:]))
    return df
                
                

    
    
    
    
    
    
    
    
    
    
    
    