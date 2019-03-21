# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 10:18:03 2019

@author: FG577RC, Kathryn Zimmerman
"""

"""
Takes two map np arrays of equal length (recordID and cluster number) and 
compares the clusters.
returns any clusters which were inconsistent between the two mappings  
"""

"""Input:
    [res] : 2D array of size Nx2, res[:,0] -> recordID, res[:,1] -> duplicate number
creates two dictionaries: 
    [clustMap] {key: first recordID in a cluster, value: recordIDs of all points in cluster}
    [grp_to_key] {key: cluster number, value: recordIDs in that cluster}
"""
import numpy as np
import pandas as pd

"""
Input:
    [res1] : n x 2 array 1 to 1 mapping of recordID to cluster number 
Output: 
    [clustMap] : Dictionary where each key is a recordID and the value is 
        a list of all the recordIDs assigned to that cluster.
"""
def clusterMap(res1):
    # dict of firstRecID: other recIDs in group
    clustMap = {}
    grp_to_key = {}
    for i in range(len(res1)):
        if res1[i,1] != "" and res1[i,1] != "0":
            if res1[i,1] not in grp_to_key: # if res1 clustnum not in lookup
                grp_to_key[res1[i,1]] = res1[i,0] # add clustnum and identifying recordID 
                clustMap[res1[i,0]] = [res1[i,0]] # add identifying recordID to cluster mapping
            else: # res1 clust num in lookup
                key = grp_to_key.get(res1[i,1]) # get identifying recordID
                clustMap[key].append(res1[i,0]) # append curr recordID to cluster list
    return clustMap
    
  

"""
    Takes RecordID cluster inputs and outputs list of 'mismatch' recordIDs
"""
def clusterCompare(base, sec):
    assert (len(base) >= len(sec)), "Base must be longer than sec"
    assert (type(base) == dict) and (type(sec) == dict)
    bad_base = set()
    not_accessed = sec.keys()
    #print "KEYS",not_accessed
    for recordID in base:
        if recordID in sec: #if same recordID in both dictionaries
            not_accessed.remove(recordID)
            # compare the list
            if base[recordID] != sec[recordID]: #if recordIDs in clusters dont match
                bad_base = bad_base.union(set(base[recordID]).union(sec[recordID]))
        else: #if recordID not in both dictionaries
            bad_base = bad_base.union(base[recordID]) # union recordIDs to bad list, dont want dups
    # bad_base has all recordIDs for clusters in base which mismatch to sec
    # not_accessed only contains identifying recordIDs for clusters in sec not
    # accessed during crawl through base 
    for key in not_accessed:
        #print "KEY",key
        bad_base = bad_base.union(sec[key])
        #print "BAD",bad_base
    # now bad_base contains all of the mismatches from both ends    
    
    return list(bad_base)


"""
    Input: 
        [recID] : list of recordIDs returned by DBSCAN
        [clustNum] : list of Cluster Numbers returned by DBSCAN
        [clustSize] : size of clusters over which to be flagged
    Return:
        List of RecordIDs which were in clusters over clustSize
"""
def largeClusters(recID, clustNum, clustSize = 4):
    recID = recID.tolist()
    curNum = 0
    count = 0
    firstInd = 0
    selectedRecs = []
    for i in range(len(clustNum)): 
        if clustNum[i] != curNum:
            curNum = clustNum[i]
            if count >= clustSize:
                lstInd = firstInd + count
                selectedRecs += recID[firstInd:lstInd]
            curNum = clustNum[i]
            count = 1
            firstInd = i
        else:
            count += 1
    return selectedRecs
                

"""
    takes two cluster assignments (on the same input data) and returns a list
    of recordIDs which were assigned to clusters differently by the two 
    approaches
"""
def clusterDiff(r1_clust, r2_clust):
    assert (type(r1_clust) == dict) and (type(r2_clust) == dict), "Parameters must be dictionaries"
    bad_recID = []
    if len(r1_clust) >= len(r2_clust):
        bad_recID = clusterCompare(r1_clust, r2_clust)
    else:
        bad_recID = clusterCompare(r2_clust, r1_clust)
    return bad_recID

"""
Input: 
    [recIDs] len k list of record IDs
    [data] nxd array with last column recordIDs
Output: kxd array with only the rows of 'data' corresponding to 'recIDs'
"""
def selectRecords(recIDs, data):
    mismatchData = []
    data2 = list(data[:,-1])
    #recordIDs = recIDs.astype(int)
    print "RecordID length: ", len(recIDs)
    for record in recIDs:
        if record in data2:
            dataIndex = data2.index(record)
            row = data[dataIndex,:] # verified this is pulling correctly
            mismatchData.append(row)
    return np.asarray(mismatchData)
    

"""
Input: 
    [recIDs] len k list of record IDs
    [data] nxd array with last column recordIDs
Output: kxd array with only the rows of 'data' corresponding to 'recIDs'
"""
def selectRecords2(recIDs, data, SAPdata):
    mismatchData = []
    #recordIDs = recIDs.astype(int)
    print "RecordID length: ", len(recIDs)
    for record in recIDs:
        dataIndex = np.where(data[:,-1] == record)
        #print "index: ", dataIndex
        row = data[dataIndex]
        #print "row: ", row[0]
        mismatchData.append(row[0])
    return np.asarray(mismatchData)
    

# load clusterings
"""
Inputs:
    [epsilon] : epsilon used to generate clusters (do we want this??)
    [mapping] : string, name of csv file with the cluster numbers       
    [two_groups] : 
    [first] : indicates if this is the first run of verify on this data
Returns: saves two excel files into Vendor folder
    "Mismatch_Clusters_{epsilon}.csv"
    "Large_Clusters_{epsilon}.csv"
"""
def verify(epsilon, mapping, two_groups=True, first=True):
    assert type(mapping) == str, "Mapping, second attribute, must be a string"
    fullMap = pd.read_csv(mapping, dtype=str)
    num_rows, num_cols = fullMap.shape
    colNames = fullMap.columns.values.tolist()
    clust1Num = fullMap.iloc[:,0].to_numpy()
    #recordID = fullMap.iloc[:,-1].to_numpy() #instead of pulling recID, assign new
    recordID = range(num_rows)
    
    if first:
        clust2Num = fullMap.iloc[:,1].to_numpy() #comparing first and second cols
        data = fullMap.iloc[:,2:].to_numpy()
    else:
        clust2Num = fullMap.iloc[:,2].to_numpy() # comparing first and third cols
        data = fullMap.iloc[:,3:].to_numpy()    

    # build inputs to clusterMap()
    rid_clust1 = np.transpose(np.asarray([recordID,clust1Num]))
    rid_clust2 = np.transpose(np.asarray([recordID,clust2Num]))

    # build cluter map dicitonary
    clustDict = clusterMap(rid_clust)
    groupDict = clusterMap(rid_group)

    # find cluster mismatches (list of recordIDs)
    mismatch = clusterDiff(clustDict, groupDict)
    print "number of mismatched records: ", len(mismatch)

    # create mismatch dataframe
    data = fullMap.to_numpy()
    fullData = selectRecords(mismatch, data)
    print "full data shape: ", fullData.shape 
    df = pd.DataFrame(fullData, columns=colNames)
    df.to_csv("Mismatch_Clusters_"+str(epsilon)+".csv", sep=',', index=False)

    # find large clusters, create and save dataset
    largeClust = selectRecords(largeClusters(rid_clust[:,0], 
                                             rid_clust[:,1]),data)
    df = pd.DataFrame(largeClust, columns=colNames)
    df.to_csv("Large_Clusters_"+str(epsilon)+".csv", sep=',', index=False)
    print "Verification Complete"
    

"""
Inputs:
    [fullMap] : string, name of csv file with full data set and cluster nums
    [clusterMap] : string, name of csv file with truncated dataset and 
        cluster numbers     
    [SAPMap] : string, name of csv file with SAP group numbers
    [column] : the column name or index (0 justified) which contains the 
        clusters to be compared against the SAP grouping
    [recordID] : the column name or index(0 justified) which contains the
        unique identifier for each record
    [SAPrecordID] : column name or index (0 justified) which contains the
        unique identifier for each record
    [SAPgroup] : column name or index (0 justified) which contains the SAP 
        grouping numbers
Returns: saves two pandas DataFrames:
    The mismatched clusters
    Clusters which contain greater than 3 records
"""
def verify2(fullMap,clustMap,SAPMap, column, recordID, SAPrecordID,SAPgroup):
    assert type(clustMap) == str, "Mapping, second attribute, must be a string"
    assert type(SAPMap) == str, "Mapping, second attribute, must be a string"
    clustMap = pd.read_csv(clustMap, dtype=str)
    num_rows, num_cols = clustMap.shape
    colNames = clustMap.columns.values.tolist()
    if type(column) == int:
        clust = clustMap.columns(column)
    clust1Num = clustMap[column].to_numpy()
   
    #recordID is the column name it is a string
    if type(recordID) == int:
        recordID = clustMap.columns[recordID]
    recID = clustMap[recordID].to_numpy()
    data = clustMap.drop(recordID,axis=1).to_numpy()
    
    # where we pull in SAP data
    SAPmap = pd.read_csv(SAPMap,  dtype='str', keep_default_na=False)
    print SAPmap.head(5)
    if type(SAPgroup) == int:
        SAPgroup = SAPmap.columns(SAPgroup)
    clust2Num = SAPmap[SAPgroup].to_numpy() # pulling in SAP groupings
    if type(SAPrecordID) == int:
        SAPrecordID = SAPmap.columns[SAPrecordID]
    SAPrecID = SAPmap[SAPrecordID].to_numpy()
    
    # build inputs to clusterMap() 
    # now these arrays are not the same length eep!
    rid_clust1 = np.transpose(np.asarray([recID,clust1Num]))
    rid_clust2 = np.transpose(np.asarray([SAPrecID,clust2Num]))
    #print "clusters: ", rid_clust1
    #print "groups: ", rid_clust2


    # build cluster map dicitonary
    clustDict = clusterMap(rid_clust1)
    #print "clusterDict: ", clustDict
    groupDict = clusterMap(rid_clust2)
    #print "group dict: ", groupDict
    
    # find cluster mismatches (list of recordIDs)
    mismatch = clusterDiff(clustDict, groupDict)
    print "number of mismatched records: ", len(mismatch)

    # create mismatch dataframe
    FullMap = pd.read_csv(fullMap, dtype=str) # has all the data pts
    cols = list(FullMap.columns.values) #Make a list of all of the columns in the df
    cols.pop(cols.index(recordID)) #Remove recordID from list
    cols = cols+[recordID]
    df = FullMap[cols] #Create new dataframe with recId last
    fullData = selectRecords(mismatch, df.to_numpy())
    print "full data shape: ", fullData.shape 
    df = pd.DataFrame(fullData, columns=cols)
    ind = cols.index(column)
    cols[ind] = "Compared: " + column
    df.columns = cols
    cols2 = cols[:ind+1]+[SAPgroup]+ cols[ind+1:]
    df = df[cols2]
    print "Verification Complete"
    return df
    


 
        
   

        
    
    