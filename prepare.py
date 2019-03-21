# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 11:08:01 2019

@author: FG577RC, Kathryn Zimmerman
"""

# Customer Clustering

import numpy as np
import pandas as pd
import nltk
from sklearn import feature_extraction
import matplotlib.pyplot as plt

from nltk.stem import WordNetLemmatizer
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def myTokenizer(s):
    stopwords = nltk.corpus.stopwords.words('english')
    s = s.lower() # downcase
    tokens = nltk.word_tokenize(s)
    tokens = [t for t in tokens if len(t) > 2] # remove short words
    tokens = [wordnet_lemmatizer.lemmatize(t) for t in tokens] # lemmatize 
    tokens = [t for t in tokens if t not in stopwords] # remove stopwords 
    #tokens = [t for t in tokens if not any(c.isdigit() for c in t)] # remove any digits, i.e. "3rd edition"
    return tokens
 
"""
input: [s] string
returns: s without leading digits and space
"""
def removeDigits(s):
    s = str(s)
    for i in range(len(s)):
        if s[i].isalpha():
            return s[i:]
        if s[i] == ' ':
            return s[i+1:]
    return s

"""
input: [s] string to be cleansed
output: s with expanded lagging cardinal directions and no spaces for anything 
        before the cardinal directions
"""
def cleanse(s):
    s = unicode(s, errors='ignore')
    cardDir = {' N':' North', ' S':' South',' E':' East',' W':' West',
               ' NE':' Northeast', ' NW':' Northwest',' SE':' Southeast', 
               ' SW':' Southwest'}
    if (s[-2:] in cardDir):
        return s[:-2].replace(' ','') + cardDir[s[-2:]]        
    elif (s[-3:] in cardDir):
        return s[:-3].replace(' ','') + cardDir[s[-3:]]
    else:
        return s.replace(' ','')
"""
input:
    [addresses] nx1 list of first line of addresses in dataset
returns:
    nx1 list of addresses with house number removed, cardinal directions 
    expanded to full name and spaces removed
    e.g. 1145 Highway 6 N -> Highway6 North
         5604 Highmont Ave -> Highmont
"""
def cleanAddress(addresses):
    cleaned = []
    for address in addresses:
        cleaned.append(cleanse(removeDigits(address)))
    return cleaned


# converts NxD matrix to Nx1 matrix with string inputs and each value
# previously stored in separate columns separated by a space
# allows data to be treated as natural language data
def preprocess(dataset):
    num_rows, num_cols = np.shape(dataset)
    newData = []
    num_exception = 0
    success = 0
    for row in xrange(num_rows):
        # create a single string and tokenize
        sent = ''
        for col in xrange(num_cols):
            try:
                cell = unicode(dataset[row,col], errors='ignore')
                sent += ' ' + cell
                success += 1
            except Exception as e:
                #print "exception", e
                num_exception += 1
        sent = sent.strip()
        newData.append(sent)
    return newData





