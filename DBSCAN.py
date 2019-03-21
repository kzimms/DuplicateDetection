# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 13:45:31 2019

@author: FG577RC, Kathryn Zimmerman

using a csv of preprocessed data, this script performs DBSCAN clustering
to find matches in the data set
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


"""
Function which returns the number of features necessary to account for n % of the 
variance in unstructured TF-IDF data.
Input  :
Return : number of features (segmented data?)

"""
def explainedVar(n, data_variance):
    exp_var = 0
    ind = 0
    while exp_var < n:
        exp_var += data_variance[ind]
        ind += 1
        print str(n*100)+"% of data variance explained with PCA features: ", ind
        return ind

# DBSCAN
"""
Input:
    [PCA] : N x D matrix composed of N samples of D-Dimensional feature vectors
    [recID] : list of recordIDs that correspond to the feature vectors in each
        row of the PCA matrix
    [epsilon] : density value for DBSCAN algorithm
Returns: Nx2 array of RecordID to Cluster mapping
"""
def clusterDBSCAN(PCA, recID, epsilon):
    from sklearn.cluster import DBSCAN
    cluster_ind = DBSCAN(eps=epsilon, min_samples=2, metric='cosine').fit_predict(PCA) + 1
    #comparison file of assigned groups vs expected
    comp = np.transpose(np.asarray([recID, cluster_ind]))
    print "cluster: ",comp
    np.savetxt("Clusters_Mapping.csv", comp, delimiter=",", fmt='%s')
    return comp

def DBSCAN(PCA, epsilon):
    from sklearn.cluster import DBSCAN
    cluster_ind = DBSCAN(eps=epsilon, min_samples=2, metric='cosine').fit_predict(PCA) + 1
    #comparison file of assigned groups vs expected
    comp = np.transpose(np.asarray(cluster_ind))
    print "cluster: ",comp
    #np.savetxt("Clusters_Mapping.csv", comp, delimiter=",", fmt='%s')
    return comp




