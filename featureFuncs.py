# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 11:07:45 2019

@author: FG577RC, Kathryn Zimmerman
This file contains all the code for making features for the Supervised ML task
"""

import params
from nltk.tokenize.api import TokenizerI
import textdistance

"""
Returns a list of columns names pertaining to desired features
"""
def getFeatures():
    return params.col_to_func.keys().append('Label')

"""
input:
    [row1] : a record for comparison
    [row2] : a second record for comparison
    [lst] : a list of strings representing column names
returns:
    The normalized Jaro-Winkler distance between the concatenation of all the 
    columns specified in [lst] in the two rows.
"""
def nameJW(row1,row2,lst):
    name1 = ''
    name2 = ''
    for col in lst:
        name1 = name1 + ' ' + row1.loc[col].strip()
        name2 = name2 + ' ' + row2.loc[col].strip()
    feature = textdistance.JaroWinkler.jaro_winkler.normalized_distance(name1,name2)
    return feature

"""
input:
    [row1] : a record for comparison
    [row2] : a second record for comparison
    [lst] : a list of strings representing column names
returns:
    The normalized Jaro-Winkler distance between the concatenation of all the 
    columns specified in [lst] in the two rows.
"""
def stAddressJW(row1, row2, lst):
    stAddress1 = ''
    stAddress2 = ''
    for col in lst:
        stAddress1 = stAddress1 + ' ' + row1.loc[col].strip()
        stAddress2 = stAddress2 + ' ' + row2.loc[col].strip()
    feature = textdistance.JaroWinkler.jaro_winkler.normalized_distance(stAddress1,stAddress2)
    return feature

"""
input:
    [row1] : a record for comparison
    [row2] : a second record for comparison
    [lst] : a list of strings representing column names
returns:
    The normalized Jaro-Winkler distance between the concatenation of all the 
    columns specified in [lst] in the two rows.
"""
def cityJW(row1, row2, lst):
    city1 = ''
    city2 = ''
    for col in lst:
        city1 = city1 + ' ' + row1.loc[col].strip()
        city2 = city2 + ' ' + row2.loc[col].strip()
    feature = textdistance.JaroWinkler.jaro_winkler.normalized_distance(city1,city2)
    return feature

"""
input:
    [row1] : a record for comparison
    [row2] : a second record for comparison
    [lst] : a list of strings representing column names
returns:
    a 0 or a 1 depending on if the concatenation of all the columns in the two 
    rows match
"""
def sameState(row1, row2, lst):
    state1 = ''
    state2 = ''
    feature = 0
    for col in lst:
        state1 = state1 + ' ' + row1.loc[col].strip()
        state2 = state2 + ' ' + row2.loc[col].strip()
    if state1 == state2:
        feature = 1
    return feature

"""
input:
    [row1] : a record for comparison
    [row2] : a second record for comparison
    [lst] : a list of strings representing column names
returns:
    a 0 or a 1 depending on if the concatenation of all the columns in the two 
    rows match
"""
def sameZip(row1,row2,lst):
    zip1 = ''
    zip2 = ''
    feature = 0
    for col in lst:
        zip1 = zip1 + ' ' + row1.loc[col].strip()
        zip2 = zip2 + ' ' + row2.loc[col].strip()
    if zip1 == zip2:
        feature = 1
    return feature

"""
inputs:
    [tfidf1] : tfidf vector for a row
    [tfidf2] : tfidf vector for a row
returns:
    The cosine similarity between the two tfidf vectors
"""
def cosineSim(tfidf1, tfidf2):
    return textdistance.Cosine.cosine.distance(tfidf1,tfidf2) 

"""
input:
    [row1] : a record for comparison
    [row2] : a second record for comparison
    [lst] : a list of strings representing column names
returns:
    a 0 or a 1 depending on if the concatenation of all the columns in the two 
    rows match
"""
def nameExact(row1,row2, lst):
    #combine all name cols then compare strings
    name1 = ''
    name2 = ''
    feature = 0
    for col in lst:
        name1 = name1 + ' ' + row1.loc[col].strip()
        name2 = name2 + ' ' + row2.loc[col].strip()
    if name1 == name2:
        feature = 1
    return feature

"""
input:
    [row1] : a record for comparison
    [row2] : a second record for comparison
    [lst] : a list of strings representing column names
returns:
    a 0 or a 1 depending on if the concatenation of all the columns in the two 
    rows match
"""
def stAddressExact(row1,row2, lst):
    #combine all name cols then compare strings
    address1 = ''
    address2 = ''
    feature = 0
    for col in lst:
        address1 = address1 + ' ' + row1.loc[col].strip()
        address2 = address2 + ' ' + row2.loc[col].strip()
    if address1 == address2:
        feature = 1
    return feature

"""
input:
    [row1] : a record for comparison
    [row2] : a second record for comparison
    [lst] : a list of strings representing column names
returns:
    a 0 or a 1 depending on if the concatenation of all the columns in the two 
    rows match
"""
def cityExact(row1,row2, lst):
    #combine all name cols then compare strings
    city1 = ''
    city2 = ''
    feature = 0
    for col in lst:
        city1 = city1 + ' ' + row1.loc[col].strip()
        city2 = city2 + ' ' + row2.loc[col].strip()
    if city1 == city2:
        feature = 1
    return feature

def labels(row1, row2, lst):
    label1 = row1.loc[lst[0]].strip()
    label2 = row2.loc[lst[0]].strip()
    if label1 == label2:
        return 1
    else:
        return 0
    

"""
inputs:
    [row1] : a record for comparison
    [row2] : a second record for comparison
    [tfidf1] : tfidf vector for a row
    [tfidf2] : tfidf vector for a row
returns:
    A feature vector computed via all the feature functions listed in the
    col_to_func dictionary between row1 and row2.
"""
def makeFeatures(row1,row2, tfidf1, tfidf2):
    features = getFeatures()
    featureVector = []
    for feat in features:
        func = params.col_to_func[feat][0]
        if len(params.col_to_func[feat]) > 1:
            lst = params.col_to_func[feat][1:]
            featureVector.append(func(row1,row2,lst))
        else:
            featureVector.append(func(tfidf1,tfidf2))
    return featureVector


