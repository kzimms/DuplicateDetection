# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:57:04 2019

@author: FG577RC, Kathryn Zimmerman 
Master Parameter File
"""

import featureFuncs

# TF-IDF parameters
max_df = 0.3
min_df = 2
max_features = 100000
n_gram = 1
language = 'English'

# Supervised Learning parameters
features = featureFuncs.getFeatures()
# dictionary that maps column names to the functions that define them 
feat_dictionary = {}

col_to_func = {
        'Name_JW': [featureFuncs.nameJW, 'NAME1','NAME2','NAME3','NAME4'],
        'St_Address_JW': [featureFuncs.stAddressJW,'STRAS'],
        'City_JW' : [featureFuncs.cityJW,'ORTO1'],
        'Same_State': [featureFuncs.sameState,'REGIO'],
        'Same_Zip': [featureFuncs.sameZip,'PSTLZ'],
        'Cosine_Sim': [featureFuncs.cosineSim],
        'Name_Exact': [featureFuncs.nameExact,'NAME1','NAME2','NAME3','NAME4'],
        'St_Address_Exact': [featureFuncs.stAddressExact,'STRAS'],
        'City_Exact': [featureFuncs.cityExact,'ORTO1'],
        'Label': [featureFuncs.label, 'Eps: 0.01']
        }