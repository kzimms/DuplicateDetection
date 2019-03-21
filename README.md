# Duplicate Detection 
### Via Data Similarity Mapping

Due to poor and varied governance across heritage systems, master data was highly inconsistent within and across systems. Differences in encoding conventions complicate the use of out-of-the-box SAP tools for duplicate detection.

The implementation of an unsupervised machine learning model allows duplicate detection without comprehensive (or any) data cleansing on data that may end up being culled or consolidated. This approach is effective for any application in which similar natural language data records need to be grouped together at varying levels of granularity. 


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

This project was coded in Python 2.7 although, with minor modifications, could be run in Python 3.6. The below pre-requisites assume the user has a current version of pip installed. 

### Prerequisites

Python 2.7

```
Python --version
2.7.15
```

pip 

```
pip --version
pip 9.0.3 from c:\python27\lib\site-packages (python 2.7)
```
pip will allow you to easily download all of the dependencies for this code base. pip should install when you download python. However, if it does not, follow the download directions here: https://packaging.python.org/tutorials/installing-packages/

The packages and dependencies of this project are:
NumPy, SciPy, Pandas, MatPlotLib, NLTK, PyHDB, scikit-learn

If you do not have one of these installed please install via pip:
```
pip install {package name}
```


### Running the Scripts

A step by step series of examples that tell you how to get a development env running

If you already have csv files of data that you wish to find duplicates in, skip to the next step. If your data is not saved in a HANA database, you will need to write your own script to either pull it into a pandas dataframe or save it to a csv and then start from the next step. 

To pull in data from HANA and save it as a csv file, edit the top of Hana_query.py, save it, and run in the command line. The first four lines provide the necessary information to connect to the correct HANA server. The fifth line specifies a SQL query to run on the HANA server to create the desired datatable. The last two lines refer to your local machine and specify the folder and file name for the datatable to be saved. 

```
######### ALL CHANGES IN THIS BLOCK ###########################
HANAhost = "XX.XXX.XX.XXX"      # put host number in "quotes"
HANAport = 30115                # keep port number as integer
HANAuser = ""             # put username in "quotes"
HANApassword = ""     # put password in "quotes"
SQLquery = ""         # SQL query that would be used in HANA to access data
masterData = ""         # Folder where the data will be saved
fileName = ""           # base of the file name where pull will be saved
###############################################################
```
In the command line run:
```
python Hana_query.py
```

If the data you pulled in has multiple languages or is vastly different based on a single indicator (such as country code) run the below script. If not, skip to the next step. This script is tailored to HANA master basic datatables; however, small changes would make this script more generalizable. 

In the script, edit the following lines so the code points to the desired files.
```
######### ALL CHANGES IN THIS BLOCK ###########################
filePath = "FolderName"           # Folder name where files stored
fileList = ["FileName1","FileName2"]   # List of file names without .csv ending that contain the data and need to be combined
###############################################################

```
In the command line run:
```
python createRegions.py
```

This step de-structures the rencords and runs TF-IDF on the result. The TF-IDF vectors are then run through DBSCAN clustering with cosine similarity distance measure. Cosine similarity was chosen to reduce errors due to the potential high dimensionality of the data. 

Edit the top of the file as directed,

```
######### ALL CHANGES IN THIS BLOCK ###########################
filePath = "Vendor"           # Folder name where files stored
region = "NAmerica"             # Region from files created in createRegions.
num_features = 500000           # max number of features to be created during TF-IDF. If this gets maxed out, increase it.
epsilons = [0.05, 0.12,0.15]     # list of different levels of granularity for duplicates to be found. Lower the epsilon, the more similar returned results will be.
###############################################################
```
If your desired file was not produced by createRegions.py, edit the below line of code:
```
df = pd.read_csv("../"+filePath+"/{YOUR FILE NAME}.csv", dtype='str', keep_default_na=False)

```
In the command line run:
```
python dedup.py
```
This will save two files in the specified folder. The first is the complete dataset with an additional column of cluster numbers for each value of epsilon. The second only contains records which were identified as 'non-unique'. For large datasets this makes manual review and point testing more manageable. 

To make a comparison between two runs of clustering or between clustering results and SAP grouping results, you will need to edit the top of the file. This script was written with the assumption that the comparison would be between SAP grouping results and a clustering column result. If you would like to compare between two clustering columns, set the SAP variables to correspond to the desired cluster column. 
```
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
```
And run in the command line:
```
python compare.py
```
This will save a csv of the mismatched clusters.
## Authors

* **Kathryn Zimmerman** 

## Acknowledgments

* Deepak Nagarajan for his thoughts and insights as this solution came together. 
